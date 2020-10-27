using OpenCvSharp;

namespace IGemDetector
{
    public class DetectResult
    {
        public string Name { get; set; }
        public string Type { get; set; }
        public Rect BoundingBox { get; set; }
    }
}