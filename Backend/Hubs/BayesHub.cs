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
        Task ReceiveParameters(double[] param);
        Task ReceiveFinalResult(double target, double[] param);
    }

    public class BayesHub : Hub<IBayesClientInterface>
    {
        private static readonly ConcurrentDictionary<string, (Process Process, int Count)> sessions = new ();

        public async Task Start(int num, int count)
        {
            var connId = Context.ConnectionId;
            sessions[connId] = (Process.Start(new ProcessStartInfo
            {
                FileName = "python",
                Arguments = "bayes.py",
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                WorkingDirectory = "./bayes",
                StandardInputEncoding = Encoding.Default,
                StandardOutputEncoding = Encoding.Default
            }), count);
            sessions[connId].Process.Exited += (obj, e) =>
            {
                if (obj is Process p)
                {
                    p.Dispose();
                    sessions.TryRemove(connId, out _);
                }
            };
            await sessions[connId].Process.StandardInput.WriteLineAsync(num.ToString());
            await sessions[connId].Process.StandardInput.WriteLineAsync(count.ToString());
            var str = await sessions[connId].Process.StandardOutput.ReadLineAsync();
            var param = str.Split(" ", StringSplitOptions.RemoveEmptyEntries).Select(i => double.Parse(i)).ToArray();
            await Clients.Client(connId).ReceiveParameters(param);
        }

        public async Task ProvideResult(float target)
        {
            var session = sessions[Context.ConnectionId];
            session.Count--;
            sessions[Context.ConnectionId] = session;
            await session.Process.StandardInput.WriteLineAsync(target.ToString());
            var str = await session.Process.StandardOutput.ReadLineAsync();
            var param = str.Split(" ", StringSplitOptions.RemoveEmptyEntries).Select(i => double.Parse(i)).ToArray();
            if (session.Count >= 0)
            {
                await Clients.Client(Context.ConnectionId).ReceiveParameters(param);
            }
            else
            {
                await Clients.Client(Context.ConnectionId).ReceiveFinalResult(param[0], param[1..]);
            }
        }
    }
}
