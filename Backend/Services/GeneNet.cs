using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace IGemDetector
{
    public class GeneNet
    {
        public static readonly ConcurrentDictionary<string, Task<List<List<float>>>> StartTasks = new();
        public static readonly ConcurrentDictionary<string, Task<string>> SearchTasks = new();

        public static string StartSearchGeneNet(GeneNetSearchRequest model, DbConfig config)
        {
            var id = Guid.NewGuid().ToString().Replace("-", "");
            SearchTasks[id] = Task.Run(async () =>
            {
                using var process = Process.Start(new ProcessStartInfo
                {
                    FileName = "./genenet/search",
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true
                });
                await process.StandardInput.WriteLineAsync(model.Matrix.Count.ToString());
                await process.StandardInput.WriteLineAsync(model.InitSeqLen.ToString());
                foreach (var line in model.Matrix)
                {
                    await process.StandardInput.WriteLineAsync(string.Join(" ", line.Select(i => i.ToString())));
                }
                using var cts = new CancellationTokenSource();
                cts.CancelAfter(10 * 1000 * 60);
                try
                {
                    await process.WaitForExitAsync(cts.Token);
                    if (process.ExitCode != 0)
                    {
                        return "{\"failed\": true}";
                    }
                    var result = await process.StandardOutput.ReadToEndAsync();
                    return result;
                }
                catch
                {
                    try
                    {
                        process.Kill();
                    }
                    catch
                    {
                        // ignored
                    }
                    return "{\"failed\": true}";
                }
            });
            return id;
        }

        public static string StartGeneNet(GeneNetTaskRequest model)
        {
            var id = Guid.NewGuid().ToString().Replace("-", "");
            StartTasks[id] = Task.Run(async () =>
            {
                await File.WriteAllTextAsync($"./genenet/{id}.genenet", string.Join(",", model.Curve.Select(i => i.ToString())));
                using var process = Process.Start(new ProcessStartInfo
                {
                    FileName = "python",
                    ArgumentList = {
                        "GeneNetTF.py",
                        model.Species.ToString(),
                        model.Iterations.ToString(),
                        model.Regularize ? "1" : "0",
                        model.Prune ? "1" : "0",
                        model.PruneLimit.ToString(),
                        model.Start.ToString(),
                        model.End.ToString(),
                        $"{id}.genenet"
                    },
                    WorkingDirectory = "./genenet",
                    RedirectStandardOutput = true,
                    StandardOutputEncoding = Encoding.Default
                });
                await process.WaitForExitAsync();
                var output = await process.StandardOutput.ReadToEndAsync();
                var matrix = new List<List<float>>();
                foreach (var i in output.Split("\n"))
                {
                    if (i.StartsWith("RM"))
                    {
                        var line = i.Trim()[3..^1];
                        matrix.Add(line.Split(",").Select(j => float.Parse(j.Trim())).ToList());
                    }
                }
                try
                {
                    File.Delete($"./genenet/{id}.genenet");
                }
                catch
                {
                    // ignored
                }
                return matrix;
            });
            return id;
        }
    }
}
