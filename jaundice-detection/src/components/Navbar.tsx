import { Link, useLocation } from "react-router-dom";
import { Heart } from "lucide-react";

const Navbar = () => {
  const location = useLocation();
  
  const isActive = (path: string) => location.pathname === path;
  
  return (
    <nav className="bg-card border-b border-border sticky top-0 z-50 backdrop-blur-sm bg-card/95">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 group">
            <div className="bg-primary/10 p-2 rounded-lg group-hover:bg-primary/20 transition-colors">
              <Heart className="h-6 w-6 text-primary" />
            </div>
            <span className="text-xl font-bold text-foreground">JaundiceCare</span>
          </Link>
          
          <div className="flex gap-1">
            <Link
              to="/"
              className={`px-2 sm:px-4 py-2 rounded-lg transition-all text-sm sm:text-base ${
                isActive("/")
                  ? "bg-primary text-primary-foreground font-medium"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted"
              }`}
            >
              Home
            </Link>
            <Link
              to="/detect"
              className={`px-2 sm:px-4 py-2 rounded-lg transition-all text-sm sm:text-base ${
                isActive("/detect")
                  ? "bg-primary text-primary-foreground font-medium"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted"
              }`}
            >
              Detect
            </Link>
            <Link
              to="/about"
              className={`px-2 sm:px-4 py-2 rounded-lg transition-all text-sm sm:text-base ${
                isActive("/about")
                  ? "bg-primary text-primary-foreground font-medium"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted"
              }`}
            >
              About
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
