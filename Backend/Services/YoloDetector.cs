using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using OpenCvSharp;
using OpenCvSharp.Dnn;
using System.Net.Http;

namespace IGemDetector
{
    public class YoloDetector
    {
        const float confThreshold = 0F;
        const float nmsThreshold = 0F;
        const int inpWidth = 416;
        const int inpHeight = 416;
        const string modelConfig = "yolov4-custom.cfg";
        const string modelWeights = "yolov4-custom_final.weights";
        const string classesFile = "coco.names";
        static List<string> classes = new List<string>();
        static HttpClient client = new HttpClient();

        public static async Task<List<YoloResult>> Detect(Mat img)
        {
            var filename = Guid.NewGuid().ToString().Replace("-", "");
            var ret = new List<YoloResult>();
            img.SaveImage($"yolov4/{filename}.jpg");

            try
            {
                using var res = await client.GetStreamAsync($"http://localhost:5002/predict/{filename}.jpg");
                var lines = await JsonSerializer.DeserializeAsync<List<string>>(res);
                foreach (var i in lines)
                {
                    if (i.StartsWith("PRO"))
                    {
                        var entry = i.Split(" ");
                        var (l, t, r, b) = (int.Parse(entry[2]), int.Parse(entry[3]), int.Parse(entry[4]), int.Parse(entry[5]));
                        ret.Add(new YoloResult
                        {
                            ClassId = 0,
                            Confidence = float.Parse(entry[1]),
                            Region = new Rect(l, t, r - l, b - t)
                        });
                    }
                }
                File.Delete($"yolov4/{filename}.jpg");
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                Console.WriteLine(ex.StackTrace);
            }
            return ret;
        }

        public static List<YoloResult> Detect2(Mat img)
        {
            if (!File.Exists(modelConfig))
            {
                Console.WriteLine($"No cfg file.");
                return null;
            }

            if (!File.Exists(modelWeights))
            {
                Console.WriteLine($"No weights file.");
                return null;
            }

            using (var sr = new StreamReader(classesFile))
            {
                while (!sr.EndOfStream)
                {
                    classes.Add(sr.ReadLine());
                }
            }
            using var net = CvDnn.ReadNetFromDarknet(modelConfig, modelWeights);

            net.SetPreferableBackend(Net.Backend.OPENCV);
            net.SetPreferableTarget(Net.Target.OPENCL);

            using var blob = CvDnn.BlobFromImage(img, 1 / 255D, new Size(inpWidth, inpHeight), new Scalar(0, 0, 0), true, false);

            net.SetInput(blob);

            var outNames = GetOutputsNames(net);

            var outs = outNames.Select(_ => new Mat()).ToArray();

            net.Forward(outs, outNames);

            return PostProcess(img, outs);

            // var freq = Cv2.GetTickFrequency() / 1000;
            // var t = net.GetPerfProfile(out var layersTimes) / freq;
            // string label = string.Format("Inference time for a frame : {0} ms", Math.Round(t));
            // Cv2.PutText(img, label, new Point(0, 15), HersheyFonts.HersheySimplex, 0.5, Scalar.Black);
            // var detected = new Mat();
            // img.ConvertTo(detected, MatType.CV_8U);
            // Cv2.ImShow("yolov3 in C#", detected);
        }

        // Remove the bounding boxes with low confidence using non-maxima suppression
        public unsafe static List<YoloResult> PostProcess(Mat frame, Mat[] outs)
        {
            List<int> classIds = new List<int>();
            List<float> confidences = new List<float>();
            List<Rect> boxes = new List<Rect>();

            for (var i = 0; i < outs.Length; i++)
            {
                // Scan through all the bounding boxes output from the network and keep only the
                // ones with high confidence scores. Assign the box's class label as the class
                // with the highest score for the box.
                float* data = (float*)outs[i].Data.ToPointer();
                for (int j = 0; j < outs[i].Rows; ++j, data += outs[i].Cols)
                {
                    Mat scores = outs[i].Row(j).ColRange(5, outs[i].Cols);
                    Point classIdPoint;
                    double confidence;
                    // Get the value and location of the maximum score
                    Cv2.MinMaxLoc(scores, out var _, out confidence, out var _, out classIdPoint);
                    if (confidence >= confThreshold)
                    {
                        int centerX = (int)(data[0] * frame.Cols);
                        int centerY = (int)(data[1] * frame.Rows);
                        int width = (int)(data[2] * frame.Cols);
                        int height = (int)(data[3] * frame.Rows);
                        int left = centerX - width / 2;
                        int top = centerY - height / 2;

                        classIds.Add(classIdPoint.X);
                        confidences.Add((float)confidence);
                        boxes.Add(new Rect(left, top, width, height));
                    }
                }
            }

            // Perform non maximum suppression to eliminate redundant overlapping boxes with
            // lower confidences
            int[] indices;
            CvDnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold, out indices);
            var list = new List<YoloResult>();
            for (var i = 0; i < indices.Length; i++)
            {
                int idx = indices[i];
                Rect box = boxes[idx];
                // DrawPred(classIds[idx], confidences[idx], box.X, box.Y,
                //          box.X + box.Width, box.Y + box.Height, frame);
                list.Add(new YoloResult
                {
                    ClassId = classIds[idx],
                    Confidence = confidences[idx],
                    Region = box
                });
            }
            return list;
        }

        // Draw the predicted bounding box
        public static void DrawPred(int classId, float conf, int left, int top, int right, int bottom, Mat frame)
        {
            //Draw a rectangle displaying the bounding box
            Cv2.Rectangle(frame, new Point(left, top), new Point(right, bottom), new Scalar(0, 0, 255));

            //Get the label for the class name and its confidence
            string label = Math.Round(conf * 100).ToString() + " %";
            if (classes.Any())
            {
                label = classes[classId] + ":" + label;
            }

            //Display the label at the top of the bounding box
            int baseLine;
            Size labelSize = Cv2.GetTextSize(label, HersheyFonts.HersheySimplex, 0.5, 1, out baseLine);
            top = Math.Max(top, labelSize.Height);
            Cv2.PutText(frame, label, new Point(left, top), HersheyFonts.HersheySimplex, 0.5, Scalar.Black);
        }

        public static List<string> names = new List<string>();
        public static string[] GetOutputsNames(Net net)
        {
            if (!names.Any())
            {
                //Get the indices of the output layers, i.e. the layers with unconnected outputs
                var outLayers = net.GetUnconnectedOutLayers();

                //get the names of all the layers in the network
                var layersNames = net.GetLayerNames();

                // Get the names of the output layers in names
                for (var i = 0; i < outLayers.Length; i++)
                    names.Add(layersNames[outLayers[i] - 1]);
            }
            return names.ToArray();
        }
    }
}