import { useState, useRef } from "react";
import Navbar from "@/components/Navbar";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import {
  Upload,
  Loader2,
  AlertCircle,
  CheckCircle2,
  AlertTriangle,
  Camera,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { api } from "@/lib/api";

type SeverityLevel = "none" | "mild" | "moderate" | "severe";

interface AnalysisResult {
  severity: SeverityLevel;
  suggestion: string;
}

const symptoms = [
  { id: "dark-urine", label: "Dark urine", icon: "💧" },
  { id: "pale-stools", label: "Pale stools", icon: "🧻" },
  { id: "fatigue", label: "Fatigue", icon: "😴" },
  { id: "abdominal-pain", label: "Abdominal pain", icon: "🤕" },
  { id: "fever", label: "Fever", icon: "🌡️" },
  { id: "itching", label: "Itching", icon: "🙌" },
];

const Detect = () => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>("");
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [showCamera, setShowCamera] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const { toast } = useToast();

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        toast({
          title: "File too large",
          description: "Please upload an image smaller than 5MB",
          variant: "destructive",
        });
        return;
      }

      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: "user",
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setShowCamera(true);
      }
    } catch (error) {
      console.error("Camera error:", error);
      toast({
        title: "Camera access denied",
        description: "Please allow camera access to take a photo",
        variant: "destructive",
      });
    }
  };

  const capturePhoto = async () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (!video || !canvas) {
      console.error("Video or canvas ref not available");
      toast({
        title: "Error",
        description: "Camera components not ready",
        variant: "destructive",
      });
      return;
    }

    // Wait a bit for the video to be fully ready
    await new Promise((resolve) => setTimeout(resolve, 100));

    if (video.videoWidth === 0 || video.videoHeight === 0) {
      toast({
        title: "Camera not ready",
        description: "Please wait a moment and try again",
        variant: "destructive",
      });
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    if (!ctx) {
      toast({
        title: "Error",
        description: "Cannot create image",
        variant: "destructive",
      });
      return;
    }

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(
      (blob) => {
        if (blob) {
          const file = new File([blob], "camera-photo.jpg", {
            type: "image/jpeg",
          });
          const preview = canvas.toDataURL("image/jpeg");

          setSelectedImage(file);
          setImagePreview(preview);
          stopCamera();

          toast({
            title: "Photo captured!",
            description: "Eye image captured successfully",
          });
        } else {
          toast({
            title: "Error",
            description: "Failed to capture photo",
            variant: "destructive",
          });
        }
      },
      "image/jpeg",
      0.95
    );
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setShowCamera(false);
  };

  const toggleSymptom = (symptomId: string) => {
    setSelectedSymptoms((prev) =>
      prev.includes(symptomId)
        ? prev.filter((id) => id !== symptomId)
        : [...prev, symptomId]
    );
  };

  const analyzeJaundice = async () => {
    if (!selectedImage) {
      toast({
        title: "Missing image",
        description: "Please upload an eye image first",
        variant: "destructive",
      });
      return;
    }

    setIsAnalyzing(true);
    setResult(null);

    try {
      // Call the real Python backend API
      const prediction = await api.predict(selectedImage);

      // Map API response to our severity levels
      let severity: SeverityLevel = "none";
      const symptomCount = selectedSymptoms.length;

      if (prediction.prediction === "jaundice") {
        // Jaundice detected
        if (prediction.confidence >= 0.9) {
          severity = symptomCount >= 3 ? "severe" : "moderate";
        } else if (prediction.confidence >= 0.7) {
          severity = "moderate";
        } else {
          severity = "mild";
        }
      } else {
        // No jaundice detected
        if (symptomCount >= 4) {
          severity = "moderate"; // Symptoms present but no jaundice in eyes
        } else if (symptomCount >= 2) {
          severity = "mild";
        } else {
          severity = "none";
        }
      }

      // Generate appropriate suggestion
      let suggestion = "";
      if (prediction.prediction === "jaundice") {
        if (severity === "severe") {
          suggestion = `Jaundice detected with ${(
            prediction.confidence * 100
          ).toFixed(
            1
          )}% confidence. Multiple symptoms present. Please seek immediate medical attention from a healthcare professional. This requires urgent evaluation and treatment.`;
        } else if (severity === "moderate") {
          suggestion = `Jaundice indicators detected with ${(
            prediction.confidence * 100
          ).toFixed(
            1
          )}% confidence. We recommend consulting a healthcare provider soon for proper evaluation and liver function tests.`;
        } else {
          suggestion = `Mild jaundice indicators detected with ${(
            prediction.confidence * 100
          ).toFixed(
            1
          )}% confidence. Monitor your symptoms and consider scheduling a medical consultation for further assessment.`;
        }
      } else {
        if (symptomCount >= 4) {
          suggestion = `No jaundice detected in eye image (${(
            prediction.probability_normal * 100
          ).toFixed(
            1
          )}% confidence), but multiple symptoms are present. Please consult a healthcare provider for proper evaluation.`;
        } else if (symptomCount >= 2) {
          suggestion = `No jaundice detected in eye image (${(
            prediction.probability_normal * 100
          ).toFixed(
            1
          )}% confidence). Some symptoms present - stay hydrated, rest well, and monitor your condition. Consult a doctor if symptoms persist.`;
        } else {
          suggestion = `No jaundice detected with ${(
            prediction.probability_normal * 100
          ).toFixed(
            1
          )}% confidence. Continue monitoring your health and maintain a healthy lifestyle with proper hydration and nutrition.`;
        }
      }

      setResult({ severity, suggestion });

      toast({
        title: "Analysis Complete",
        description: `${
          prediction.prediction === "jaundice"
            ? "Jaundice detected"
            : "No jaundice detected"
        } (${(prediction.confidence * 100).toFixed(1)}% confidence)`,
      });
    } catch (error) {
      console.error("Analysis error:", error);

      toast({
        title: "API Error",
        description:
          error instanceof Error
            ? error.message
            : "Failed to analyze image. Please ensure the backend server is running.",
        variant: "destructive",
      });

      // Fallback to symptom-based analysis
      const symptomCount = selectedSymptoms.length;
      let severity: SeverityLevel = "none";
      let suggestion = "";

      if (symptomCount === 0) {
        severity = "none";
        suggestion =
          "Unable to connect to AI model. Based on no symptoms, continue monitoring your health. Please try again when the backend is available.";
      } else if (symptomCount <= 2) {
        severity = "mild";
        suggestion =
          "Backend unavailable. Based on mild symptoms, stay hydrated and rest. Please start the backend server for AI analysis.";
      } else if (symptomCount <= 4) {
        severity = "moderate";
        suggestion =
          "Backend unavailable. Based on moderate symptoms, we recommend consulting a healthcare provider. Please start the backend server for AI analysis.";
      } else {
        severity = "severe";
        suggestion =
          "Backend unavailable. Based on severe symptoms, please seek immediate medical care. Start the backend server for AI-powered analysis.";
      }

      setResult({ severity, suggestion });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const restartTest = () => {
    setSelectedImage(null);
    setImagePreview("");
    setSelectedSymptoms([]);
    setResult(null);
    stopCamera();
  };

  const getSeverityConfig = (severity: SeverityLevel) => {
    const configs = {
      none: {
        icon: CheckCircle2,
        color: "text-primary",
        bg: "bg-primary/10",
        title: "No Jaundice Detected",
      },
      mild: {
        icon: AlertCircle,
        color: "text-medical-yellow",
        bg: "bg-medical-yellow/20",
        title: "Mild Jaundice Indicators",
      },
      moderate: {
        icon: AlertTriangle,
        color: "text-yellow-600",
        bg: "bg-yellow-100",
        title: "Moderate Jaundice Symptoms",
      },
      severe: {
        icon: AlertTriangle,
        color: "text-destructive",
        bg: "bg-destructive/10",
        title: "Severe Jaundice Symptoms",
      },
    };
    return configs[severity];
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="container mx-auto px-4 py-8 sm:py-12">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-8 sm:mb-10 animate-fade-in">
            <h1 className="text-3xl sm:text-4xl font-bold text-foreground mb-3 px-4">
              Jaundice Detection
            </h1>
            <p className="text-sm sm:text-base text-muted-foreground px-4">
              Upload your eye image and select symptoms for analysis
            </p>
          </div>

          {!result ? (
            <div className="space-y-6 sm:space-y-8">
              {/* Image Upload Section */}
              <Card className="p-6 sm:p-8 animate-slide-up">
                <h2 className="text-xl sm:text-2xl font-semibold text-foreground mb-4 sm:mb-6 flex items-center gap-2">
                  <Upload className="h-6 w-6 text-primary" />
                  Upload Eye Image
                </h2>

                <div className="space-y-4">
                  {showCamera ? (
                    <div className="relative">
                      <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        className="w-full h-64 object-cover rounded-xl bg-black"
                      />
                      <canvas ref={canvasRef} className="hidden" />
                      <div className="flex gap-2 mt-4">
                        <Button
                          onClick={capturePhoto}
                          variant="medical"
                          className="flex-1"
                        >
                          <Camera className="mr-2 h-4 w-4" />
                          Capture Photo
                        </Button>
                        <Button
                          onClick={stopCamera}
                          variant="outline"
                          className="flex-1"
                        >
                          Cancel
                        </Button>
                      </div>
                    </div>
                  ) : !imagePreview ? (
                    <div className="space-y-3">
                      <label className="flex flex-col items-center justify-center w-full h-48 border-2 border-dashed border-border rounded-xl cursor-pointer bg-muted/30 hover:bg-muted/50 transition-colors">
                        <div className="flex flex-col items-center justify-center pt-5 pb-6">
                          <Upload className="h-10 w-10 text-muted-foreground mb-2" />
                          <p className="mb-1 text-sm text-foreground font-medium">
                            Upload from gallery
                          </p>
                          <p className="text-xs text-muted-foreground">
                            JPG or PNG (MAX. 5MB)
                          </p>
                        </div>
                        <input
                          type="file"
                          className="hidden"
                          accept="image/jpeg,image/png"
                          onChange={handleImageUpload}
                        />
                      </label>

                      <div className="relative">
                        <div className="absolute inset-0 flex items-center">
                          <span className="w-full border-t border-border" />
                        </div>
                        <div className="relative flex justify-center text-xs uppercase">
                          <span className="bg-background px-2 text-muted-foreground">
                            or
                          </span>
                        </div>
                      </div>

                      <Button
                        onClick={startCamera}
                        variant="outline"
                        className="w-full h-48 border-2 border-dashed border-primary/50 bg-primary/5 hover:bg-primary/10"
                      >
                        <div className="flex flex-col items-center">
                          <Camera className="h-10 w-10 text-primary mb-2" />
                          <p className="mb-1 text-sm text-foreground font-medium">
                            Take photo with camera
                          </p>
                          <p className="text-xs text-muted-foreground">
                            Use your device camera
                          </p>
                        </div>
                      </Button>
                    </div>
                  ) : (
                    <div className="relative">
                      <img
                        src={imagePreview}
                        alt="Uploaded eye"
                        className="w-full h-64 object-cover rounded-xl"
                      />
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => {
                          setSelectedImage(null);
                          setImagePreview("");
                        }}
                        className="absolute top-2 right-2"
                      >
                        Change Image
                      </Button>
                    </div>
                  )}
                </div>
              </Card>

              {/* Symptoms Section */}
              <Card
                className="p-6 sm:p-8 animate-slide-up"
                style={{ animationDelay: "0.1s" }}
              >
                <h2 className="text-xl sm:text-2xl font-semibold text-foreground mb-4 sm:mb-6">
                  Select Your Symptoms
                </h2>

                <div className="grid sm:grid-cols-2 gap-4">
                  {symptoms.map((symptom) => (
                    <div
                      key={symptom.id}
                      className={`flex items-center space-x-3 p-4 rounded-lg border-2 transition-all cursor-pointer ${
                        selectedSymptoms.includes(symptom.id)
                          ? "border-primary bg-primary/5"
                          : "border-border hover:border-primary/50 hover:bg-muted/50"
                      }`}
                      onClick={() => toggleSymptom(symptom.id)}
                    >
                      <Checkbox
                        id={symptom.id}
                        checked={selectedSymptoms.includes(symptom.id)}
                        onCheckedChange={() => toggleSymptom(symptom.id)}
                      />
                      <Label
                        htmlFor={symptom.id}
                        className="flex items-center gap-2 cursor-pointer flex-1"
                      >
                        <span className="text-xl">{symptom.icon}</span>
                        <span className="text-foreground">{symptom.label}</span>
                      </Label>
                    </div>
                  ))}
                </div>
              </Card>

              {/* Analyze Button */}
              <div className="flex justify-center animate-fade-in">
                <Button
                  variant="medical"
                  size="lg"
                  onClick={analyzeJaundice}
                  disabled={isAnalyzing || !selectedImage}
                  className="w-full sm:w-auto"
                >
                  {isAnalyzing ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    "Analyze Jaundice"
                  )}
                </Button>
              </div>
            </div>
          ) : (
            /* Results Section */
            <div className="space-y-6 animate-fade-in">
              <Card className="p-6 sm:p-8">
                {(() => {
                  const config = getSeverityConfig(result.severity);
                  const Icon = config.icon;

                  return (
                    <>
                      <div className="flex items-center gap-3 sm:gap-4 mb-6">
                        <div className={`${config.bg} p-2 sm:p-3 rounded-xl`}>
                          <Icon
                            className={`h-6 w-6 sm:h-8 sm:w-8 ${config.color}`}
                          />
                        </div>
                        <div>
                          <h2 className="text-xl sm:text-2xl font-bold text-foreground">
                            {config.title}
                          </h2>
                          <p className="text-sm sm:text-base text-muted-foreground">
                            Analysis Complete
                          </p>
                        </div>
                      </div>

                      <div className="bg-muted/30 rounded-xl p-4 sm:p-6 mb-6">
                        <h3 className="font-semibold text-foreground mb-3">
                          Recommendation:
                        </h3>
                        <p className="text-sm sm:text-base text-foreground leading-relaxed">
                          {result.suggestion}
                        </p>
                      </div>

                      <div className="flex items-start gap-3 bg-accent/50 p-4 rounded-lg">
                        <AlertCircle className="h-5 w-5 text-foreground flex-shrink-0 mt-0.5" />
                        <p className="text-sm text-foreground">
                          Remember: This is a screening tool. Always consult a
                          healthcare professional for proper diagnosis and
                          treatment.
                        </p>
                      </div>
                    </>
                  );
                })()}
              </Card>

              <div className="flex justify-center">
                <Button
                  variant="outline"
                  size="lg"
                  onClick={restartTest}
                  className="w-full sm:w-auto"
                >
                  Restart Test
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Detect;
