using System.Collections.Generic;
using OpenCvSharp;

namespace IGemDetector
{
    public class Result
    {
        public string Language { get; set; }
        public double TextAngle { get; set; }
        public string Orientation { get; set; }
        public List<Region> Regions { get; set; }
    }

    public class Region
    {
        public string BoundingBox { get; set; }
        public List<Line> Lines { get; set; }
    }

    public class Line
    {
        public string BoundingBox { get; set; }
        public List<Word> Words { get; set; }
    }

    public class Word
    {
        public string BoundingBox { get; set; }
        public string Text { get; set; }
    }
    
    public class OcrResult
    {
        public Rect Region { get; set; }
        public string Text { get; set; }
    }
}