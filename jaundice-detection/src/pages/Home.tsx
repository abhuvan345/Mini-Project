import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Eye, Shield, Activity, AlertCircle } from "lucide-react";
import Navbar from "@/components/Navbar";
import heroImage from "@/assets/hero-eye.jpg";

const Home = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-medical-mint-light via-background to-medical-yellow/30 -z-10" />
        <div className="container mx-auto px-4 py-12 sm:py-16 md:py-24">
          <div className="grid md:grid-cols-2 gap-8 md:gap-12 items-center">
            <div className="animate-fade-in">
              <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-4 sm:mb-6 leading-tight">
                JaundiceCare: Early Detection, Safer Health
              </h1>
              <p className="text-base sm:text-lg text-muted-foreground mb-6 sm:mb-8 leading-relaxed">
                Upload an eye image and share your symptoms to know your jaundice severity. 
                Our AI helps you stay informed and safe with compassionate, instant analysis.
              </p>
              <Link to="/detect">
                <Button variant="medical" size="lg" className="group">
                  Start Test
                  <Eye className="ml-2 h-5 w-5 group-hover:scale-110 transition-transform" />
                </Button>
              </Link>
            </div>
            
            <div className="animate-slide-up">
              <div className="relative rounded-2xl overflow-hidden shadow-2xl">
                <img 
                  src={heroImage} 
                  alt="Healthy eye illustration" 
                  className="w-full h-auto"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12 sm:py-16 bg-muted/30">
        <div className="container mx-auto px-4">
          <h2 className="text-2xl sm:text-3xl font-bold text-center mb-8 sm:mb-12 text-foreground">
            How JaundiceCare Helps You
          </h2>
          <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8">
            <div className="bg-card p-6 rounded-2xl shadow-md hover:shadow-lg transition-all animate-fade-in">
              <div className="bg-medical-mint/10 w-14 h-14 rounded-lg flex items-center justify-center mb-4">
                <Eye className="h-7 w-7 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-foreground">Visual Analysis</h3>
              <p className="text-muted-foreground">
                Upload a clear eye photo for AI-powered detection of jaundice indicators.
              </p>
            </div>
            
            <div className="bg-card p-6 rounded-2xl shadow-md hover:shadow-lg transition-all animate-fade-in" style={{ animationDelay: "0.1s" }}>
              <div className="bg-medical-yellow/50 w-14 h-14 rounded-lg flex items-center justify-center mb-4">
                <Activity className="h-7 w-7 text-secondary-foreground" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-foreground">Symptom Check</h3>
              <p className="text-muted-foreground">
                Share your symptoms for a comprehensive health assessment and severity rating.
              </p>
            </div>
            
            <div className="bg-card p-6 rounded-2xl shadow-md hover:shadow-lg transition-all animate-fade-in" style={{ animationDelay: "0.2s" }}>
              <div className="bg-medical-blue/10 w-14 h-14 rounded-lg flex items-center justify-center mb-4">
                <Shield className="h-7 w-7 text-medical-blue" />
              </div>
              <h3 className="text-xl font-semibold mb-3 text-foreground">Instant Guidance</h3>
              <p className="text-muted-foreground">
                Receive immediate, personalized recommendations based on your results.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Disclaimer Footer */}
      <footer className="bg-card border-t border-border py-6 sm:py-8">
        <div className="container mx-auto px-4">
          <div className="flex items-start gap-3 max-w-3xl mx-auto bg-accent/50 p-4 sm:p-6 rounded-xl">
            <AlertCircle className="h-5 w-5 text-foreground flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-foreground mb-1">Medical Disclaimer</p>
              <p className="text-sm text-muted-foreground">
                This tool is for screening purposes only and should not replace professional medical advice. 
                Always consult a healthcare provider for proper diagnosis and treatment.
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;
