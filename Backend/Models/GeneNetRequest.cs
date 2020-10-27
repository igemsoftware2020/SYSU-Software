using System.Collections.Generic;

namespace IGemDetector
{
    public class GeneNetSearchRequest
    {
        public int InitSeqLen { get; set; }
        public List<List<float>> Matrix { get; set; }
    }
    public class GeneNetTaskRequest
    {
        public int Species { get; set; }
        public int Iterations { get; set; }
        public bool Regularize { get; set; }
        public bool Prune { get; set; }
        public float PruneLimit { get; set; } = 1;
        public float Start { get; set; }
        public float End { get; set; }
        public List<float> Curve { get; set; }
    }

    public class GeneNetResultRequest
    {
        public string Id { get; set; }
    }
}
