using System.Collections.Generic;
using OpenCvSharp.Aruco;

namespace IGemDetector.Simulation
{
    public class LineEntry
    {
        public int Start { get; set; }
        public int End { get; set; }
        public string Type { get; set; }
    }
    public class SimulationInputModel
    {
        public Dictionary<int, double> Parts { get; set; }
        public Dictionary<int, double> Ks { get; set; }
        public Dictionary<int, double> Ns { get; set; }
        public Dictionary<int, double> Ds { get; set; }
        public List<LineEntry> Lines { get; set; }
        public double Time { get; set; }
        public string Target { get; set; }
        public double TargetAmount { get; set; }
        public string Type { get; set; }
    }
}