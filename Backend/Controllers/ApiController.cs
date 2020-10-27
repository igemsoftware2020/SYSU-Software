using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using IGemDetector.Simulation;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using OpenCvSharp;

namespace IGemDetector.Controllers
{
    [Route("")]
    public class HomeController : ControllerBase
    {
        [Route("")]
        [Route("index")]
        public string Index() => "SYSU-Software IGem 2020 backend server";
    }

    [ApiController]
    [Route("api")]
    public class ApiController : ControllerBase
    {
        public ApiController(IOptions<DbConfig> config)
        {
            this.config = config.Value;
        }
        private readonly static JsonSerializerOptions options = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
            DictionaryKeyPolicy = JsonNamingPolicy.CamelCase
        };
        private readonly DbConfig config;

        [HttpGet, Route("genenet_s_res")]
        public object RequestGeneNetSearchResult(string id)
        {
            if (GeneNet.SearchTasks.ContainsKey(id) && GeneNet.SearchTasks[id].IsCompleted)
            {
                Console.WriteLine(GeneNet.SearchTasks[id].Result);
                return JsonSerializer.Deserialize<object>(GeneNet.SearchTasks[id].Result);
            }
            return JsonSerializer.Deserialize<object>("{}");
        }

        [HttpPost, Route("genenet_s_req")]
        public GeneNetIdResponse RequestGeneNetSearchTask([FromBody] GeneNetSearchRequest model)
        {
            return new GeneNetIdResponse { Id = GeneNet.StartSearchGeneNet(model, config) };
        }

        [HttpGet, Route("genenet_res")]
        public GeneNetResultResponse RequestGeneNetResult(string id)
        {
            if (GeneNet.StartTasks.ContainsKey(id) && GeneNet.StartTasks[id].IsCompleted)
            {
                return new GeneNetResultResponse { Finished = true, Matrix = GeneNet.StartTasks[id].Result };
            }
            return new GeneNetResultResponse { Finished = false };
        }

        [HttpPost, Route("genenet_req")]
        public GeneNetIdResponse RequestGeneNetTask([FromBody] GeneNetTaskRequest model)
        {
            return new GeneNetIdResponse { Id = GeneNet.StartGeneNet(model) };
        }

        [HttpPost, Route("simulate")]
        public async Task<object> SimulateAsync([FromBody] SimulationInputModel data)
        {
            var str = JsonSerializer.Serialize(data, options);
            var result = await SimAndOpt.SimAndOptAsync(str);
            return JsonSerializer.Deserialize<object>(result, options);
        }

        [HttpPost, Route("detect")]
        public async Task<List<List<DetectResult>>> DetectAsync(IFormFile file)
        {
            await using var fs = file.OpenReadStream();
            const int LINE_DY = 100;
            // using var svm = Model.Load("model.xml");
            using var image = Mat.FromStream(fs, ImreadModes.Color);
            // var ratio = image.Width / 800.0;
            // if (image.Height / 600.0 > ratio) ratio = image.Height / 600.0;
            // Cv2.Resize(image, image, new Size(image.Width / ratio, image.Height / ratio));
            var yolo = YoloDetector.Detect(image);
            var sel = Cv2.GetStructuringElement(MorphShapes.Rect, new Size(4, 2));
            // 输入图片
            // Cv2.ImShow("input image", image);
            using var processed = image
                .CvtColor(ColorConversionCodes.BGR2GRAY)
                .AdaptiveThreshold(255, AdaptiveThresholdTypes.GaussianC, ThresholdTypes.BinaryInv, 51, 27)
                .MorphologyEx(MorphTypes.Gradient, sel)
                .Threshold(127, 255, ThresholdTypes.BinaryInv);
            // Cv2.ImShow("processed image", processed);
            processed.FindContours(out var contours, out var hierarchies, RetrievalModes.Tree, ContourApproximationModes.ApproxNone);

            // using var contourMat = image.Clone();
            // for (var i = 0; i < contours.Length; i++)
            // {
            //     Cv2.DrawContours(contourMat, contours, i, Scalar.Red, 1, LineTypes.Link8, hierarchies);
            //     // if (Cv2.ContourArea(contours[i]) < 400) continue;
            //     // var rect = Cv2.BoundingRect(contours[i]);
            //     // Cv2.Rectangle(image, rect, Scalar.Green, 2);
            //     // using var m = image.Clone(rect);
            //     // if (Convert.ToInt32(Model.Predict(svm, m)) == 1)
            //     // {
            //     //     Cv2.Rectangle(image, rect, Scalar.Red, 2);
            //     // }
            // }
            // Cv2.ImShow("contours", contourMat);

            // Cv2.WaitKey();

            using var img = image
                .CvtColor(ColorConversionCodes.BGR2GRAY)
                .AdaptiveThreshold(255, AdaptiveThresholdTypes.GaussianC, ThresholdTypes.BinaryInv, 51, 27)
                .Threshold(127, 255, ThresholdTypes.BinaryInv);

            var result1 = OcrDetector.OcrDetectImage(image);
            var result2 = OcrDetector.OcrDetectImage(img);
            var results = await Task.WhenAll(new[] { result1, result2 });
            var ocrResult = results[0].Regions.Count >= results[1].Regions.Count ? results[0] : results[1];
            var ocr = OcrDetector.Mark(img, ocrResult).ToList();

            List<object> merged = new List<object>();
            foreach (var i in await yolo) if (i.ClassId == 0) merged.Add(i);
            foreach (var i in ocr) merged.Add(i);

            #region FUS
            var father = new int[merged.Count];
            int Find(object x)
            {
                var index = merged.IndexOf(x);
                return father[index] == index ? index : Find(merged[father[index]]);
            }

            void Union(object x, object y)
            {
                var index1 = Find(x);
                var index2 = Find(y);
                father[index1] = index2;
            }

            for (var i = 0; i < merged.Count; i++) father[i] = i;
            #endregion

            string GetTypeNameFromText(string text)
            {
                var pattern = text.ToLowerInvariant().Trim();
                if (pattern.StartsWith("pro") ||
                    pattern.StartsWith("pr0") ||
                    pattern.StartsWith("dro") ||
                    pattern.StartsWith("dr0")) return "PRO";
                if (pattern.StartsWith("rbs") || pattern.StartsWith("bbs")) return "RBS";
                if (pattern.StartsWith("ter")) return "TER";
                return "CDS";
            }

            bool IsNearBy(Rect x, Rect y)
            {
                var cx1 = x.Top + x.Height / 2;
                var cx2 = y.Top + y.Height / 2;
                var cy1 = x.Left + x.Width / 2;
                var cy2 = y.Left + y.Width / 2;
                var dis = Math.Sqrt(Math.Pow(cx2 - cx1, 2) + Math.Pow(cy2 - cy1, 2));
                return dis < 100;
            }

            foreach (var i in merged)
            {
                foreach (var j in merged)
                {
                    var item1Y = i switch
                    {
                        YoloResult y => y.Region.Top + y.Region.Height / 2,
                        OcrResult o => o.Region.Top + o.Region.Height / 2,
                        _ => throw new InvalidDataException()
                    };

                    var item2Y = j switch
                    {
                        YoloResult y => y.Region.Top + y.Region.Height / 2,
                        OcrResult o => o.Region.Top + o.Region.Height / 2,
                        _ => throw new InvalidDataException()
                    };

                    if (Math.Abs(item1Y - item2Y) <= LINE_DY)
                    {
                        Union(i, j);
                    }
                }
            }

            var dict = new Dictionary<int, List<object>>();
            foreach (var i in merged)
            {
                var index = Find(i);
                if (!dict.ContainsKey(index)) dict[index] = new List<object>();
                dict[index].Add(i);
            }

            var all = new List<List<DetectResult>>();
            var alphabets = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890";
            foreach (var l in dict)
            {
                all.Add(new List<DetectResult>());
                var index = all.Count - 1;
                foreach (var i in l.Value.OrderBy(j => (j switch
                {
                    YoloResult y => y.Region.Left + y.Region.Width / 2,
                    OcrResult o => o.Region.Left + o.Region.Width / 2,
                    _ => throw new InvalidDataException()
                })))
                {
                    try
                    {
                        all[index].Add(i switch
                        {
                            YoloResult y => new DetectResult
                            {
                                Name = "PRO",
                                Type = "PRO",
                                BoundingBox = y.Region
                            },
                            OcrResult o => new DetectResult
                            {
                                Name = (string.IsNullOrWhiteSpace(o.Text) || o.Text.Length < 3 || !alphabets.Contains(o.Text[0]))
                                    ? throw new InvalidDataException() : o.Text,
                                Type = GetTypeNameFromText(o.Text),
                                BoundingBox = o.Region
                            },
                            _ => throw new InvalidDataException()
                        });
                    }
                    catch
                    {
                        continue;
                    }
                }

                for (int i = 0; i < all[index].Count; i++)
                {
                    if (all[index][i].Name == "PRO" && all[index][i].Type == "PRO")
                    {
                        if (i < all[index].Count - 1 && all[index][i + 1].Type == "PRO" &&
                            IsNearBy(all[index][i].BoundingBox, all[index][i + 1].BoundingBox))
                        {
                            all[index].Remove(all[index][i]);
                            i--;
                            continue;
                        }
                        if (i > 0 && all[index][i - 1].Type == "PRO" &&
                            IsNearBy(all[index][i].BoundingBox, all[index][i - 1].BoundingBox))
                        {
                            all[index].Remove(all[index][i]);
                            i--;
                            continue;
                        }
                    }
                }
            }

            foreach (var seq in all)
            {
                foreach (var ele in seq)
                {
                    ele.Type = ele.Type switch
                    {
                        "CDS" => "cds",
                        "PRO" => "promoter",
                        "RBS" => "rbs",
                        "TER" => "terminator",
                        _ => "unknown"
                    };
                }
            }

            return all;
        }
    }
}
