using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading.Tasks;

namespace IGemDetector
{
    public class SimAndOpt
    {
        public static async Task<string> SimAndOptAsync(string input)
        {
            var filename = Guid.NewGuid().ToString().Replace("-", "") + ".json";
            await File.WriteAllTextAsync(Path.Combine("simulation", filename), input);
            using var process = Process.Start(new ProcessStartInfo
            {
                FileName = "python",
                Arguments = $"sim_and_opt.py {filename}",
                WorkingDirectory = "./simulation",
                RedirectStandardOutput = true,
                StandardOutputEncoding = Encoding.Default,
                UseShellExecute = false
            });
            await process.WaitForExitAsync();
            var str = await process.StandardOutput.ReadToEndAsync();
            foreach (var i in str.Split("\n", StringSplitOptions.RemoveEmptyEntries))
            {
                if (i.StartsWith("{\"series")) return i;
            }
            try
            {
                File.Delete(Path.Combine("simulation", filename));
            }
            catch
            {
                //ignored 
            }
            return "{}";
        }
    }
}
