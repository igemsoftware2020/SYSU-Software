using System.Collections.Generic;

namespace IGemDetector
{
    public class GeneNetResultResponse
    {
        public bool Finished { get; set; }
        public List<List<float>> Matrix { get; set; }
    }

    public class GeneNetIdResponse
    {
        public string Id { get; set; }
    }
}