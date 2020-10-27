using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using OpenCvSharp;

namespace IGemDetector
{
    public class OcrDetector
    {
        private static readonly HttpClient client = new HttpClient();
        
        public static (int L, int T, int W, int H) GetBoundingBox(string box)
        {
            var s = box.Split(",");
            if (s.Length != 4) throw new InvalidDataException();
            return (int.Parse(s[0]), int.Parse(s[1]), int.Parse(s[2]), int.Parse(s[3]));
        }

        public static async Task<Result> OcrDetectImage(Mat image)
        {
            using var stream = image.ToMemoryStream(".jpg");
            var uri = new Uri("https://igem-cv.cognitiveservices.azure.com/vision/v3.0/ocr?language=en&detectOrientation=true");
            using var message = new StreamContent(stream);
            message.Headers.Add("Content-Type", "application/octet-stream");
            message.Headers.Add("Ocp-Apim-Subscription-Key", "7a1e5b105c9b4a24b93cec62589ed96e");
            var res = await client.PostAsync(uri, message);
            var result = await res.Content.ReadAsStreamAsync();
            return await JsonSerializer.DeserializeAsync<Result>(result, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
        }

        public static IEnumerable<OcrResult> Mark(Mat image, Result result)
        {
            foreach (var i in result.Regions)
            {
                var box = GetBoundingBox(i.BoundingBox);
                // Cv2.Rectangle(image, new OpenCvSharp.Rect(box.L, box.T, box.W, box.H), Scalar.Red, 1);
                foreach (var j in i.Lines)
                {
                    var innerBox = GetBoundingBox(j.BoundingBox);
                    // Cv2.Rectangle(image, new OpenCvSharp.Rect(innerBox.L, innerBox.T, innerBox.W, innerBox.H), Scalar.Blue, 1);
                    foreach (var k in j.Words)
                    {
                        var wordBox = GetBoundingBox(k.BoundingBox);
                        var rect = new Rect(wordBox.L, wordBox.T, wordBox.W, wordBox.H);
                        // Cv2.Rectangle(image, rect, Scalar.DarkGreen, 1);
                        // var text = FilterAnsiString(k.Text);
                        if (string.IsNullOrWhiteSpace(k.Text)) continue;
                        // Cv2.PutText(image, text, new Point(wordBox.L, wordBox.T), HersheyFonts.HersheyPlain, 1, Scalar.DarkOrange, 1);
                        yield return new OcrResult
                        {
                            Region = rect,
                            Text = k.Text
                        };
                    }
                }
            }
        }
    }
}