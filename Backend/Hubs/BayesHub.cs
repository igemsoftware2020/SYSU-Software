using System;
using System.Collections.Concurrent;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.SignalR;

namespace IGemDetector
{
    public interface IBayesClientInterface
    {
        Task ReceiveParameters(float x, float y);
        Task ReceiveFinalResult(float target, float x, float y);
    }

    public class BayesHub : Hub<IBayesClientInterface>
    {
        private static readonly ConcurrentDictionary<string, Process> sessions = new ConcurrentDictionary<string, Process>();

        public async Task Start(int num, int count)
        {
            var connId = Context.ConnectionId;
            sessions[connId] = Process.Start(new ProcessStartInfo
            {
                FileName = "python",
                Arguments = "bayes.py",
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                WorkingDirectory = "./bayes",
                StandardInputEncoding = Encoding.Default,
                StandardOutputEncoding = Encoding.Default
            });
            sessions[connId].Exited += (obj, e) =>
            {
                if (obj is Process p)
                {
                    p.Dispose();
                    sessions.TryRemove(connId, out _);
                }
            };
            await sessions[connId].StandardInput.WriteLineAsync(count.ToString());
            await sessions[connId].StandardInput.WriteLineAsync(num.ToString());
            var str = await sessions[connId].StandardOutput.ReadLineAsync();
            var param = str.Split(" ", StringSplitOptions.RemoveEmptyEntries).Select(i => float.Parse(i)).ToList();
            await Clients.Client(connId).ReceiveParameters(param[0], param[1]);
        }

        public async Task ProvideResult(float target)
        {
            await sessions[Context.ConnectionId].StandardInput.WriteLineAsync(target.ToString());
            var str = await sessions[Context.ConnectionId].StandardOutput.ReadLineAsync();
            var param = str.Split(" ", StringSplitOptions.RemoveEmptyEntries).Select(i => float.Parse(i)).ToList();
            if (param.Count == 2)
            {
                await Clients.Client(Context.ConnectionId).ReceiveParameters(param[0], param[1]);
            }
            else
            {
                await Clients.Client(Context.ConnectionId).ReceiveFinalResult(param[0], param[1], param[2]);
            }
        }
    }
}
