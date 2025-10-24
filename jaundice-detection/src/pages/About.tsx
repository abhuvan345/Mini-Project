import Navbar from "@/components/Navbar";
import { Heart, Eye, Shield, Users, AlertCircle } from "lucide-react";
import doctorIcon from "@/assets/doctor-icon.jpg";

const About = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      <div className="container mx-auto px-4 py-8 sm:py-12">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8 sm:mb-12 animate-fade-in">
            <div className="inline-flex items-center justify-center w-16 h-16 sm:w-20 sm:h-20 bg-primary/10 rounded-2xl mb-4 sm:mb-6">
              <Heart className="h-8 w-8 sm:h-10 sm:w-10 text-primary" />
            </div>
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-foreground mb-3 sm:mb-4 px-4">
              About JaundiceCare
            </h1>
            <p className="text-base sm:text-lg text-muted-foreground px-4">
              Your compassionate companion for early jaundice detection
            </p>
          </div>

          {/* Mission Section */}
          <div className="bg-card rounded-2xl p-6 sm:p-8 shadow-md mb-6 sm:mb-8 animate-slide-up">
            <div className="flex items-center gap-4 mb-6">
              <img 
                src={doctorIcon} 
                alt="Doctor icon" 
                className="w-16 h-16 rounded-xl"
              />
              <div>
                <h2 className="text-2xl font-bold text-foreground">Our Mission</h2>
                <p className="text-muted-foreground">Health awareness for everyone</p>
              </div>
            </div>
            <p className="text-foreground leading-relaxed mb-4">
              JaundiceCare was created to make early jaundice detection accessible to everyone. 
              By combining advanced AI image analysis with symptom assessment, we help users 
              understand potential health concerns and take timely action.
            </p>
            <p className="text-foreground leading-relaxed">
              Our goal is to empower individuals with knowledge while encouraging them to seek 
              proper medical care when needed. We believe that early awareness can save lives.
            </p>
          </div>

          {/* How It Works */}
          <div className="bg-card rounded-2xl p-6 sm:p-8 shadow-md mb-6 sm:mb-8 animate-slide-up" style={{ animationDelay: "0.1s" }}>
            <h2 className="text-xl sm:text-2xl font-bold text-foreground mb-6 flex items-center gap-3">
              <Eye className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
              How It Works
            </h2>
            <div className="space-y-6">
              <div className="flex gap-4">
                <div className="bg-primary/10 rounded-lg w-10 h-10 flex items-center justify-center flex-shrink-0">
                  <span className="text-primary font-bold">1</span>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground mb-1">Upload Eye Image</h3>
                  <p className="text-sm sm:text-base text-muted-foreground">Take a clear photo of your eye and upload it to our secure platform.</p>
                </div>
              </div>
              
              <div className="flex gap-4">
                <div className="bg-primary/10 rounded-lg w-10 h-10 flex items-center justify-center flex-shrink-0">
                  <span className="text-primary font-bold">2</span>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground mb-1">Select Symptoms</h3>
                  <p className="text-sm sm:text-base text-muted-foreground">Check any symptoms you're experiencing from our comprehensive list.</p>
                </div>
              </div>
              
              <div className="flex gap-4">
                <div className="bg-primary/10 rounded-lg w-10 h-10 flex items-center justify-center flex-shrink-0">
                  <span className="text-primary font-bold">3</span>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground mb-1">AI Analysis</h3>
                  <p className="text-sm sm:text-base text-muted-foreground">Our AI analyzes your image and symptoms to determine severity level.</p>
                </div>
              </div>
              
              <div className="flex gap-4">
                <div className="bg-primary/10 rounded-lg w-10 h-10 flex items-center justify-center flex-shrink-0">
                  <span className="text-primary font-bold">4</span>
                </div>
                <div>
                  <h3 className="font-semibold text-foreground mb-1">Get Recommendations</h3>
                  <p className="text-sm sm:text-base text-muted-foreground">Receive personalized guidance on next steps for your health.</p>
                </div>
              </div>
            </div>
          </div>

          {/* Safety & Privacy */}
          <div className="bg-card rounded-2xl p-6 sm:p-8 shadow-md mb-6 sm:mb-8 animate-slide-up" style={{ animationDelay: "0.2s" }}>
            <h2 className="text-xl sm:text-2xl font-bold text-foreground mb-6 flex items-center gap-3">
              <Shield className="h-5 w-5 sm:h-6 sm:w-6 text-primary" />
              Safety & Privacy
            </h2>
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="bg-medical-mint/10 rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-primary text-xs">✓</span>
                </div>
                <p className="text-sm sm:text-base text-foreground">Your images are analyzed securely and not stored permanently</p>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-medical-mint/10 rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-primary text-xs">✓</span>
                </div>
                <p className="text-sm sm:text-base text-foreground">We use advanced AI but always recommend professional medical consultation</p>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-medical-mint/10 rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-primary text-xs">✓</span>
                </div>
                <p className="text-sm sm:text-base text-foreground">Your personal information and health data remain confidential</p>
              </div>
            </div>
          </div>

          {/* Important Disclaimer */}
          <div className="bg-accent/50 border-2 border-primary/20 rounded-2xl p-6 sm:p-8 animate-slide-up" style={{ animationDelay: "0.3s" }}>
            <div className="flex items-start gap-3 sm:gap-4">
              <AlertCircle className="h-5 w-5 sm:h-6 sm:w-6 text-foreground flex-shrink-0 mt-1" />
              <div>
                <h3 className="text-lg sm:text-xl font-bold text-foreground mb-3">Important Medical Disclaimer</h3>
                <p className="text-sm sm:text-base text-foreground leading-relaxed mb-4">
                  JaundiceCare is a screening tool designed to raise awareness and encourage timely 
                  medical consultation. It is <strong>NOT</strong> a substitute for professional medical advice, 
                  diagnosis, or treatment.
                </p>
                <p className="text-sm sm:text-base text-foreground leading-relaxed">
                  Always seek the advice of your physician or other qualified health provider with any 
                  questions you may have regarding a medical condition. Never disregard professional 
                  medical advice or delay seeking it because of information from this tool.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
