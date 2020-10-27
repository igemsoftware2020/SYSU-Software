using OpenCvSharp;

namespace IGemDetector
{
    public class YoloResult
    {
        public Rect Region { get; set; }
        public float Confidence { get; set; }
        public int ClassId { get; set; }
    }
}