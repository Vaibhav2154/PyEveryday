"use client";

import { useState, useEffect, useRef, useCallback } from "react";

const scriptCategories = [
  {
    emoji: "🤖",
    name: "Automation",
    description: "Smart scripts that work while you sleep",
    scripts: [
      "Auto Email Sender",
      "File Organizer",
      "Backup Scheduler",
      "File Renamer",
      "Folder Monitor",
    ],
    color: "from-cyan-400 to-blue-600",
    hoverColor: "hover:from-cyan-500 hover:to-blue-700",
    bgPattern:
      "linear-gradient(45deg, rgba(6,182,212,0.1) 25%, transparent 25%), linear-gradient(-45deg, rgba(6,182,212,0.1) 25%, transparent 25%)",
    icon: "⚡",
  },
  {
    emoji: "🧠",
    name: "Productivity",
    description: "Focus amplifiers for peak performance",
    scripts: [
      "Pomodoro Timer",
      "Quote Fetcher",
      "Reminder System",
      "Time Tracker",
      "Todo Manager",
    ],
    color: "from-purple-400 to-pink-600",
    hoverColor: "hover:from-purple-500 hover:to-pink-700",
    bgPattern:
      "radial-gradient(circle at 20% 50%, rgba(168,85,247,0.1) 0%, transparent 50%)",
    icon: "🚀",
  },
  {
    emoji: "🌐",
    name: "Web Scraping",
    description: "Extract gold from the digital wilderness",
    scripts: [
      "News Fetcher",
      "Weather Checker",
      "Web Scraper",
      "YouTube Downloader",
    ],
    color: "from-green-400 to-teal-600",
    hoverColor: "hover:from-green-500 hover:to-teal-700",
    bgPattern:
      "repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(34,197,94,0.1) 2px, rgba(34,197,94,0.1) 4px)",
    icon: "🌊",
  },
  {
    emoji: "⚙️",
    name: "Utilities",
    description: "Your digital Swiss Army knife",
    scripts: [
      "Age Calculator",
      "Currency Converter",
      "Password Generator",
      "Unit Converter",
    ],
    color: "from-orange-400 to-red-600",
    hoverColor: "hover:from-orange-500 hover:to-red-700",
    bgPattern:
      "conic-gradient(from 0deg, rgba(251,146,60,0.1), rgba(239,68,68,0.1), rgba(251,146,60,0.1))",
    icon: "🔧",
  },
  {
    emoji: "📊",
    name: "Data Tools",
    description: "Transform chaos into insights",
    scripts: ["Data Converter", "Data Processor", "Data Visualizer"],
    color: "from-indigo-400 to-purple-600",
    hoverColor: "hover:from-indigo-500 hover:to-purple-700",
    bgPattern:
      "linear-gradient(135deg, rgba(99,102,241,0.1) 0%, rgba(168,85,247,0.1) 100%)",
    icon: "📈",
  },
  {
    emoji: "🔐",
    name: "Security",
    description: "Your digital fortress guardian",
    scripts: ["Password Checker","File Encryptor"],
    color: "from-red-400 to-pink-600",
    hoverColor: "hover:from-red-500 hover:to-pink-700",
    bgPattern:
      "radial-gradient(ellipse at center, rgba(239,68,68,0.1) 0%, transparent 70%)",
    icon: "🛡️",
  },
  {
    emoji: "🎵",
    name: "Media",
    description: "Master of multimedia manipulation",
    scripts: ["Audio Processor", "Image Processor"],
    color: "from-yellow-400 to-orange-600",
    hoverColor: "hover:from-yellow-500 hover:to-orange-700",
    bgPattern:
      "linear-gradient(60deg, rgba(251,191,36,0.1) 25%, transparent 25%), linear-gradient(120deg, rgba(251,191,36,0.1) 25%, transparent 25%)",
    icon: "🎨",
  },
];

const terminalCommands = [
  "python automation/auto_email_sender.py --schedule daily",
  "python productivity/pomodoro_timer.py --work 25 --break 5",
  "python web_scraping/news_fetcher.py --source tech --limit 10",
  "python utilities/password_generator.py --length 16 --secure",
  "python data_tools/data_visualizer.py --input data.csv --chart bar",
  "python security/password_checker.py --file passwords.txt",
  "python media/image_processor.py --resize 1920x1080 --format jpg",
];

const floatingParticles = Array.from({ length: 20 }, (_, i) => ({
  id: i,
  x: Math.random() * 100,
  y: Math.random() * 100,
  size: Math.random() * 4 + 2,
  speed: Math.random() * 0.3 + 0.1,
  opacity: Math.random() * 0.5 + 0.3,
}));

export default function Home() {
  const [activeScript, setActiveScript] = useState(0);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isLoaded, setIsLoaded] = useState(false);
  const [terminalInput, setTerminalInput] = useState("");
  const [terminalHistory, setTerminalHistory] = useState<string[]>([]);
  const [isTerminalFocused, setIsTerminalFocused] = useState(false);
  const [currentCommand, setCurrentCommand] = useState(0);
  const [particles, setParticles] = useState(floatingParticles);
  const [hoveredCategory, setHoveredCategory] = useState<number | null>(null);
  const [typingText, setTypingText] = useState("");
  const [showCursor, setShowCursor] = useState(true);
  const heroRef = useRef<HTMLDivElement>(null);
  const [scrollY, setScrollY] = useState(0);
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);
  const [showCodeDemo, setShowCodeDemo] = useState(false);
  const [statsAnimated, setStatsAnimated] = useState(false);

  // Typing animation for terminal
  const typeText = useCallback((text: string, callback?: () => void) => {
    setTypingText("");
    let i = 0;
    const interval = setInterval(() => {
      setTypingText(text.slice(0, i + 1));
      i++;
      if (i === text.length) {
        clearInterval(interval);
        callback?.();
      }
    }, 50);
    return interval;
  }, []);

  // Animate particles
  useEffect(() => {
    const animateParticles = () => {
      setParticles((prev) =>
        prev.map((particle) => ({
          ...particle,
          y: (particle.y + particle.speed * 0.01) % 100,
          x: particle.x + Math.sin(Date.now() * 0.0001 + particle.id) * 0.02,
        }))
      );
    };

    const interval = setInterval(animateParticles, 2000);
    return () => clearInterval(interval);
  }, []);

  // Cursor blinking
  useEffect(() => {
    const interval = setInterval(() => {
      setShowCursor((prev) => !prev);
    }, 500);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    setIsLoaded(true);

    const handleScroll = () => {
      setScrollY(window.scrollY);
      // Animate stats when scrolled into view
      if (window.scrollY > window.innerHeight * 2 && !statsAnimated) {
        setStatsAnimated(true);
      }
    };

    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener("scroll", handleScroll);
    window.addEventListener("mousemove", handleMouseMove);

    return () => {
      window.removeEventListener("scroll", handleScroll);
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, [statsAnimated]);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveScript((prev) => (prev + 1) % scriptCategories.length);
      setCurrentCommand((prev) => (prev + 1) % terminalCommands.length);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  // Auto-type commands in terminal
  useEffect(() => {
    const timeout = setTimeout(() => {
      typeText(terminalCommands[currentCommand]);
    }, 1000);
    return () => clearTimeout(timeout);
  }, [currentCommand, typeText]);

  const handleTerminalSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (terminalInput.trim()) {
      setTerminalHistory((prev) => [
        ...prev,
        `$ ${terminalInput}`,
        "Command executed successfully! ✅",
      ]);
      setTerminalInput("");
    }
  };

  const handleCategoryClick = (index: number) => {
    setSelectedCategory(selectedCategory === index ? null : index);
  };

  const toggleCodeDemo = () => {
    setShowCodeDemo(!showCodeDemo);
  };

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden relative">
      {/* Animated floating particles */}
      <div className="fixed inset-0 pointer-events-none z-0">
        {particles.map((particle) => (
          <div
            key={particle.id}
            className="absolute rounded-full bg-cyan-400/20 animate-pulse"
            style={{
              left: `${particle.x}%`,
              top: `${particle.y}%`,
              width: `${particle.size}px`,
              height: `${particle.size}px`,
              opacity: particle.opacity,
              transform: `translateY(${scrollY * 0.02}px)`,
            }}
          />
        ))}
      </div>

      {/* Enhanced cursor follower with trail effect */}
      <div
        className="fixed w-8 h-8 border-2 border-cyan-400 rounded-full pointer-events-none z-50 transition-all duration-200 ease-out mix-blend-difference"
        style={{
          left: mousePosition.x - 16,
          top: mousePosition.y - 16,
          transform: `scale(${isLoaded ? 1 : 0}) ${
            hoveredCategory !== null ? "scale(1.5)" : "scale(1)"
          }`,
          borderColor: hoveredCategory !== null ? "#f59e0b" : "#06b6d4",
        }}
      >
        <div className="absolute inset-2 bg-cyan-400/30 rounded-full animate-ping"></div>
      </div>

      {/* Navigation - Enhanced floating */}
      <nav className="fixed top-6 left-1/2 transform -translate-x-1/2 z-40 bg-black/40 backdrop-blur-xl border border-cyan-500/30 rounded-full px-8 py-4 shadow-lg shadow-cyan-500/25">
        <div className="flex items-center space-x-8">
          <div className="flex items-center space-x-3 group">
            <div className="w-8 h-8 bg-gradient-to-r from-cyan-400 to-purple-600 rounded-lg flex items-center justify-center group-hover:rotate-12 transition-transform duration-300">
              <span className="text-lg">🐍</span>
            </div>
            <span className="font-bold text-xl bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              PyEveryday
            </span>
          </div>
          <div className="flex space-x-4">
            <button
              onClick={toggleCodeDemo}
              className="px-4 py-2 bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-400/30 rounded-full text-sm font-medium hover:shadow-lg hover:shadow-purple-500/25 transition-all duration-300 hover:scale-105"
            >
              {showCodeDemo ? "Hide" : "Show"} Code
            </button>
            <a
              href="https://github.com/Vaibhav2154/PyEveryday"
              target="_blank"
              rel="noopener noreferrer"
              className="px-6 py-2 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-full text-sm font-medium hover:shadow-lg hover:shadow-cyan-500/25 transition-all duration-300 hover:scale-105"
            >
              Explore Code
            </a>
          </div>
        </div>
      </nav>

      {/* Hero Section - Enhanced terminal with interactive elements */}
      <section
        ref={heroRef}
        className="h-screen flex items-center justify-center relative"
      >
        {/* Enhanced Matrix-like background */}
        <div className="absolute inset-0 overflow-hidden">
          {[...Array(100)].map((_, i) => (
            <div
              key={i}
              className="absolute text-green-500 font-mono text-xs opacity-20 animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 10}s`,
                animationDuration: `${6 + Math.random() * 6}s`,
                transform: `translateY(${scrollY * 0.02}px) rotate(${
                  Math.random() * 360
                }deg)`,
              }}
            >
              {Math.random() > 0.7
                ? ["def", "import", "python", "class", "if"][
                    Math.floor(Math.random() * 5)
                  ]
                : Math.random() > 0.5
                ? "1"
                : "0"}
            </div>
          ))}
        </div>

        {/* Glowing orbs */}
        <div className="absolute inset-0">
          <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-cyan-400/10 rounded-full blur-3xl animate-pulse"></div>
          <div
            className="absolute bottom-1/4 right-1/4 w-40 h-40 bg-purple-400/10 rounded-full blur-3xl animate-pulse"
            style={{ animationDelay: "1s" }}
          ></div>
          <div
            className="absolute top-1/2 right-1/3 w-24 h-24 bg-green-400/10 rounded-full blur-3xl animate-pulse"
            style={{ animationDelay: "2s" }}
          ></div>
        </div>

        <div className="max-w-6xl mx-auto px-4 text-center relative z-10">
          {/* Enhanced Terminal Window */}
          <div
            className={`bg-gray-900/90 backdrop-blur-lg rounded-lg border border-gray-700 shadow-2xl transition-all duration-1000 ${
              isLoaded
                ? "opacity-100 translate-y-0"
                : "opacity-0 translate-y-10"
            } hover:shadow-cyan-500/25 hover:shadow-2xl`}
          >
            {/* Terminal Header with interactive buttons */}
            <div className="flex items-center justify-between p-4 border-b border-gray-700">
              <div className="flex space-x-2">
                <button
                  className="w-3 h-3 bg-red-500 rounded-full hover:bg-red-400 transition-colors"
                  onClick={() => setTerminalHistory([])}
                ></button>
                <button className="w-3 h-3 bg-yellow-500 rounded-full hover:bg-yellow-400 transition-colors"></button>
                <button
                  className="w-3 h-3 bg-green-500 rounded-full hover:bg-green-400 transition-colors"
                  onClick={() => setIsTerminalFocused(!isTerminalFocused)}
                ></button>
              </div>
              <span className="text-gray-400 font-mono text-sm">
                user@pyeveryday:~${" "}
                {scriptCategories[activeScript].name.toLowerCase()}
              </span>
              <div className="text-xs text-gray-500">
                {new Date().toLocaleTimeString()}
              </div>
            </div>

            {/* Enhanced Terminal Content */}
            <div className="p-8 font-mono text-left max-h-96 overflow-y-auto">
              <div className="text-green-400 mb-2">
                $ python3 pyeveryday.py --initialize
              </div>
              <div className="text-cyan-400 mb-4 animate-pulse">
                🐍 PyEveryday Automation Suite v2.0.1
              </div>

              {/* Terminal History */}
              {terminalHistory.map((line, index) => (
                <div key={index} className="mb-1 text-gray-300">
                  {line}
                </div>
              ))}

              <div className="text-white mb-6">
                <div className="mb-2 flex items-center">
                  <span className="text-green-400 mr-2">▶</span>
                  Loading {scriptCategories.length} script categories
                  <div className="ml-2 flex space-x-1">
                    <div
                      className="w-1 h-1 bg-cyan-400 rounded-full animate-bounce"
                      style={{ animationDuration: "1.5s" }}
                    ></div>
                    <div
                      className="w-1 h-1 bg-cyan-400 rounded-full animate-bounce"
                      style={{
                        animationDelay: "0.15s",
                        animationDuration: "1.5s",
                      }}
                    ></div>
                    <div
                      className="w-1 h-1 bg-cyan-400 rounded-full animate-bounce"
                      style={{
                        animationDelay: "0.3s",
                        animationDuration: "1.5s",
                      }}
                    ></div>
                  </div>
                </div>
                <div className="mb-2 flex items-center">
                  <span className="text-green-400 mr-2">▶</span>
                  Found 25+ automation tools
                  <span className="ml-2 text-green-400">✓</span>
                </div>
                <div className="mb-2 flex items-center">
                  <span className="text-green-400 mr-2">▶</span>
                  Ready to transform your workflow
                  <span className="ml-2 text-green-400">✓</span>
                </div>
              </div>

              <div className="text-yellow-400 mb-4 bg-yellow-400/10 p-2 rounded border-l-4 border-yellow-400">
                <span className="flex items-center">
                  <span className="mr-2">
                    {scriptCategories[activeScript].icon}
                  </span>
                  Active Module:{" "}
                  <span className="text-cyan-400 ml-1 font-bold">
                    {scriptCategories[activeScript].name}
                  </span>
                </span>
              </div>

              <div className="text-gray-300 mb-6 bg-gray-800/50 p-3 rounded">
                <div className="text-cyan-400 text-sm mb-1">Description:</div>
                {scriptCategories[activeScript].description}
              </div>

              <div className="flex flex-wrap gap-2 mb-6">
                {scriptCategories[activeScript].scripts.map((script, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-gray-800 text-cyan-400 rounded border border-gray-600 text-sm hover:bg-gray-700 hover:border-cyan-400 transition-all duration-200 cursor-pointer"
                    onClick={() =>
                      setTerminalHistory((prev) => [
                        ...prev,
                        `$ Running ${script}...`,
                        `✅ ${script} executed successfully!`,
                      ])
                    }
                  >
                    {script}
                  </span>
                ))}
              </div>

              {/* Interactive command input */}
              <form
                onSubmit={handleTerminalSubmit}
                className="flex items-center"
              >
                <span className="text-green-400 mr-2">$</span>
                <input
                  type="text"
                  value={terminalInput}
                  onChange={(e) => setTerminalInput(e.target.value)}
                  placeholder={typingText}
                  className="bg-transparent text-green-400 outline-none flex-1 font-mono"
                  onFocus={() => setIsTerminalFocused(true)}
                  onBlur={() => setIsTerminalFocused(false)}
                />
                <span
                  className={`text-green-400 ${
                    showCursor ? "opacity-100" : "opacity-0"
                  } transition-opacity`}
                >
                  _
                </span>
              </form>
            </div>
          </div>

          {/* Enhanced Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-6 justify-center mt-12">
            <button className="group px-8 py-4 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-lg font-bold text-lg hover:shadow-lg hover:shadow-cyan-500/25 transition-all duration-300 hover:scale-105 relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-600 to-purple-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <span className="relative flex items-center space-x-2">
                <span>Initialize Scripts</span>
                <svg
                  className="w-5 h-5 group-hover:translate-x-1 transition-transform"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 7l5 5m0 0l-5 5m5-5H6"
                  />
                </svg>
              </span>
            </button>

            <a
              href="https://github.com/Vaibhav2154/PyEveryday"
              target="_blank"
              rel="noopener noreferrer"
              className="group px-8 py-4 border-2 border-cyan-400 rounded-lg font-bold text-lg hover:bg-cyan-400 hover:text-black transition-all duration-300 relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-cyan-400 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left"></div>
              <span className="relative">View Source</span>
            </a>
          </div>
        </div>
      </section>
      {/* Script Categories - Enhanced interactive hexagonal grid */}
      <section className="py-20 relative">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              Choose Your Arsenal
            </h2>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto">
              Seven powerful categories of automation tools, each designed to
              solve specific challenges in your digital workflow.
            </p>
          </div>

          {/* Enhanced Hexagonal Grid with interactions */}
          <div className="relative max-w-6xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
              {scriptCategories.map((category, index) => (
                <div
                  key={index}
                  className={`group relative overflow-hidden rounded-2xl bg-gradient-to-br ${
                    category.color
                  } p-6 hover:scale-110 transition-all duration-500 cursor-pointer ${
                    category.hoverColor
                  } ${
                    selectedCategory === index
                      ? "ring-4 ring-cyan-400 scale-105"
                      : ""
                  }`}
                  style={{
                    clipPath:
                      index % 3 === 0
                        ? "polygon(20% 0%, 80% 0%, 100% 20%, 100% 80%, 80% 100%, 20% 100%, 0% 80%, 0% 20%)"
                        : "none",
                    backgroundImage: category.bgPattern,
                  }}
                  onMouseEnter={() => setHoveredCategory(index)}
                  onMouseLeave={() => setHoveredCategory(null)}
                  onClick={() => handleCategoryClick(index)}
                >
                  {/* Animated Background overlay */}
                  <div className="absolute inset-0 bg-black/30 group-hover:bg-black/10 transition-all duration-300"></div>

                  {/* Glowing border effect */}
                  <div className="absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-white/30 transition-all duration-300"></div>

                  <div className="relative z-10">
                    <div className="flex items-center justify-between mb-4">
                      <div className="text-4xl group-hover:scale-125 group-hover:rotate-12 transition-all duration-300">
                        {category.emoji}
                      </div>
                      <div className="text-2xl opacity-50 group-hover:opacity-100 group-hover:scale-110 transition-all duration-300">
                        {category.icon}
                      </div>
                    </div>

                    <h3 className="text-xl font-bold text-white mb-3">
                      {category.name}
                    </h3>
                    <p className="text-white/90 text-sm mb-4">
                      {category.description}
                    </p>

                    <div className="space-y-2">
                      {category.scripts
                        .slice(
                          0,
                          selectedCategory === index
                            ? category.scripts.length
                            : 3
                        )
                        .map((script, scriptIndex) => (
                          <div
                            key={scriptIndex}
                            className={`text-xs text-white/80 bg-white/20 rounded px-2 py-1 backdrop-blur-sm transition-all duration-300 hover:bg-white/30 cursor-pointer transform ${
                              selectedCategory === index
                                ? "translate-x-0 opacity-100"
                                : scriptIndex >= 3
                                ? "translate-x-4 opacity-0"
                                : "translate-x-0 opacity-100"
                            }`}
                            style={{ transitionDelay: `${scriptIndex * 50}ms` }}
                            onClick={(e) => {
                              e.stopPropagation();
                              setTerminalHistory((prev) => [
                                ...prev,
                                `$ python ${category.name.toLowerCase()}/${script
                                  .toLowerCase()
                                  .replace(/\s+/g, "_")}.py`,
                                `✅ ${script} executed successfully!`,
                              ]);
                            }}
                          >
                            {script}
                          </div>
                        ))}
                      {category.scripts.length > 3 &&
                        selectedCategory !== index && (
                          <div className="text-xs text-white/60 text-center group-hover:text-white/80 transition-colors">
                            Click to see +{category.scripts.length - 3} more...
                          </div>
                        )}
                    </div>

                    {/* Interactive indicators */}
                    <div className="absolute top-2 right-2 flex space-x-1">
                      {[...Array(3)].map((_, i) => (
                        <div
                          key={i}
                          className={`w-2 h-2 rounded-full transition-all duration-300 ${
                            hoveredCategory === index
                              ? "bg-white"
                              : "bg-white/30"
                          }`}
                          style={{ animationDelay: `${i * 0.1}s` }}
                        ></div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Interactive Code Showcase with live demo */}
      <section className="py-20 relative">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold mb-6 bg-gradient-to-r from-green-400 to-cyan-400 bg-clip-text text-transparent">
              See It In Action
            </h2>
            <p className="text-xl text-gray-400">
              Real Python scripts, real automation, real results.
            </p>
          </div>

          {/* Enhanced Code Editor Mockup */}
          <div
            className={`bg-gray-800/95 backdrop-blur-lg rounded-lg overflow-hidden shadow-2xl border border-gray-700 transition-all duration-500 ${
              showCodeDemo ? "transform scale-105 shadow-cyan-500/25" : ""
            }`}
          >
            <div className="flex items-center justify-between p-4 bg-gray-900 border-b border-gray-700">
              <div className="flex space-x-2">
                <div className="w-3 h-3 bg-red-500 rounded-full hover:bg-red-400 transition-colors cursor-pointer"></div>
                <div className="w-3 h-3 bg-yellow-500 rounded-full hover:bg-yellow-400 transition-colors cursor-pointer"></div>
                <div className="w-3 h-3 bg-green-500 rounded-full hover:bg-green-400 transition-colors cursor-pointer"></div>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-gray-400 font-mono text-sm">
                  file_organizer.py
                </span>
                <div className="flex space-x-2 text-xs">
                  <span className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded">
                    Python
                  </span>
                  <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded">
                    Active
                  </span>
                </div>
              </div>
            </div>

            <div className="p-6 font-mono text-sm relative">
              {/* Line numbers */}
              <div className="absolute left-2 top-6 text-gray-600 text-xs leading-6 select-none">
                {[...Array(15)].map((_, i) => (
                  <div key={i}>{i + 1}</div>
                ))}
              </div>

              <div className="ml-8">
                <div className="text-gray-500 hover:text-gray-400 transition-colors cursor-pointer">
                  # PyEveryday - File Organizer
                </div>
                <div className="text-purple-400">
                  import{" "}
                  <span className="text-cyan-400 hover:text-cyan-300 transition-colors cursor-pointer">
                    os
                  </span>
                  ,{" "}
                  <span className="text-cyan-400 hover:text-cyan-300 transition-colors cursor-pointer">
                    shutil
                  </span>
                </div>
                <div className="text-purple-400">
                  from{" "}
                  <span className="text-cyan-400 hover:text-cyan-300 transition-colors cursor-pointer">
                    pathlib
                  </span>{" "}
                  import{" "}
                  <span className="text-cyan-400 hover:text-cyan-300 transition-colors cursor-pointer">
                    Path
                  </span>
                </div>
                <br />
                <div className="text-purple-400">
                  def{" "}
                  <span className="text-yellow-400 hover:text-yellow-300 transition-colors cursor-pointer">
                    organize_files
                  </span>
                  (<span className="text-cyan-400">directory</span>):
                </div>
                <div className="ml-4 text-gray-300">
                  <div className="text-green-400 hover:text-green-300 transition-colors cursor-pointer">
                    # Automatically sort files by type
                  </div>
                  <div>
                    <span className="text-purple-400">for</span> file{" "}
                    <span className="text-purple-400">in</span>{" "}
                    Path(directory).iterdir():
                  </div>
                  <div className="ml-4">
                    <div>
                      <span className="text-purple-400">if</span>{" "}
                      file.is_file():
                    </div>
                    <div className="ml-4">
                      <div className="hover:bg-gray-700/50 transition-colors cursor-pointer rounded px-1">
                        extension = file.suffix.lower()
                      </div>
                      <div className="hover:bg-gray-700/50 transition-colors cursor-pointer rounded px-1">
                        create_folder_and_move(file, extension)
                      </div>
                    </div>
                  </div>
                </div>
                <br />
                <div className="text-green-400 bg-green-400/10 p-2 rounded border-l-4 border-green-400 hover:bg-green-400/20 transition-colors cursor-pointer">
                  # ✨ Your messy downloads folder becomes organized in seconds!
                </div>
              </div>

              {/* Interactive execution button */}
              {showCodeDemo && (
                <div className="absolute bottom-4 right-4">
                  <button
                    className="px-4 py-2 bg-green-500 text-black rounded font-bold hover:bg-green-400 transition-all duration-300 hover:scale-105 shadow-lg"
                    onClick={() =>
                      setTerminalHistory((prev) => [
                        ...prev,
                        "$ python file_organizer.py --execute",
                        "🗂️  Organizing files...",
                        "✅ 47 files organized successfully!",
                        "📊 Created folders: Documents, Images, Videos, Others",
                      ])
                    }
                  >
                    Run Code
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Code execution stats */}
          {showCodeDemo && (
            <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                <div className="text-2xl font-bold text-green-400">1.2s</div>
                <div className="text-gray-400">Execution Time</div>
              </div>
              <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                <div className="text-2xl font-bold text-cyan-400">47</div>
                <div className="text-gray-400">Files Processed</div>
              </div>
              <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700">
                <div className="text-2xl font-bold text-purple-400">4</div>
                <div className="text-gray-400">Folders Created</div>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Enhanced Stats Dashboard with animations */}
      <section className="py-20 relative">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div
              className={`bg-gradient-to-br from-cyan-900/50 to-blue-900/50 rounded-2xl p-8 border border-cyan-500/30 backdrop-blur-sm hover:scale-105 transition-all duration-500 cursor-pointer group ${
                statsAnimated ? "animate-bounce" : ""
              }`}
            >
              <div className="relative">
                <div className="text-6xl font-bold text-cyan-400 mb-4 group-hover:scale-110 transition-transform duration-300">
                  {statsAnimated ? "25+" : "0"}
                </div>
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-cyan-400/20 rounded-full animate-ping"></div>
              </div>
              <div className="text-xl font-semibold text-white mb-2">
                Python Scripts
              </div>
              <div className="text-gray-400">Ready-to-use automation tools</div>
              <div className="mt-4 bg-cyan-400/10 rounded-lg p-2">
                <div className="flex justify-between text-sm">
                  <span>Automation</span>
                  <span className="text-cyan-400">5 scripts</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Productivity</span>
                  <span className="text-cyan-400">5 scripts</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Utilities</span>
                  <span className="text-cyan-400">4 scripts</span>
                </div>
              </div>
            </div>

            <div
              className={`bg-gradient-to-br from-purple-900/50 to-pink-900/50 rounded-2xl p-8 border border-purple-500/30 backdrop-blur-sm hover:scale-105 transition-all duration-500 cursor-pointer group ${
                statsAnimated ? "animate-bounce" : ""
              }`}
              style={{ animationDelay: "0.2s" }}
            >
              <div className="relative">
                <div className="text-6xl font-bold text-purple-400 mb-4 group-hover:scale-110 transition-transform duration-300">
                  {statsAnimated ? "7" : "0"}
                </div>
                <div
                  className="absolute -top-2 -right-2 w-6 h-6 bg-purple-400/20 rounded-full animate-ping"
                  style={{ animationDelay: "0.5s" }}
                ></div>
              </div>
              <div className="text-xl font-semibold text-white mb-2">
                Categories
              </div>
              <div className="text-gray-400">
                Covering all aspects of automation
              </div>
              <div className="mt-4 grid grid-cols-2 gap-2">
                {scriptCategories.slice(0, 4).map((cat, i) => (
                  <div
                    key={i}
                    className="bg-purple-400/10 rounded px-2 py-1 text-xs text-purple-300"
                  >
                    {cat.emoji} {cat.name}
                  </div>
                ))}
              </div>
            </div>

            <div
              className={`bg-gradient-to-br from-green-900/50 to-teal-900/50 rounded-2xl p-8 border border-green-500/30 backdrop-blur-sm hover:scale-105 transition-all duration-500 cursor-pointer group ${
                statsAnimated ? "animate-bounce" : ""
              }`}
              style={{ animationDelay: "0.4s" }}
            >
              <div className="relative">
                <div className="text-6xl font-bold text-green-400 mb-4 group-hover:scale-110 transition-transform duration-300">
                  ∞
                </div>
                <div
                  className="absolute -top-2 -right-2 w-6 h-6 bg-green-400/20 rounded-full animate-ping"
                  style={{ animationDelay: "1s" }}
                ></div>
              </div>
              <div className="text-xl font-semibold text-white mb-2">
                Possibilities
              </div>
              <div className="text-gray-400">
                Unlimited automation potential
              </div>
              <div className="mt-4 space-y-2">
                <div className="flex items-center text-sm">
                  <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                  <span>Email automation</span>
                </div>
                <div className="flex items-center text-sm">
                  <div
                    className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"
                    style={{ animationDelay: "0.3s" }}
                  ></div>
                  <span>File management</span>
                </div>
                <div className="flex items-center text-sm">
                  <div
                    className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"
                    style={{ animationDelay: "0.6s" }}
                  ></div>
                  <span>Data processing</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Enhanced Call to Action - Interactive */}
      <section className="py-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-900/20 to-purple-900/20"></div>

        {/* Interactive background elements */}
        <div className="absolute inset-0">
          {[...Array(10)].map((_, i) => (
            <div
              key={i}
              className="absolute rounded-full bg-gradient-to-r from-cyan-400/10 to-purple-400/10 animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                width: `${20 + Math.random() * 60}px`,
                height: `${20 + Math.random() * 60}px`,
                animationDelay: `${Math.random() * 8}s`,
                animationDuration: `${4 + Math.random() * 4}s`,
              }}
            />
          ))}
        </div>

        <div className="relative max-w-4xl mx-auto text-center px-4">
          <div className="bg-gray-900/90 backdrop-blur-xl rounded-3xl p-12 border border-gray-700 hover:border-cyan-500/50 transition-all duration-500 group">
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/5 to-purple-500/5 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

            <div className="relative z-10">
              <h2 className="text-5xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent group-hover:scale-105 transition-transform duration-300">
                Ready to Automate?
              </h2>
              <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
                Join the automation revolution. Download, customize, and deploy
                Python scripts that work 24/7 for you.
              </p>

              {/* Interactive feature highlights */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <div className="bg-gray-800/50 rounded-lg p-4 hover:bg-gray-700/50 transition-all duration-300 cursor-pointer group/feature">
                  <div className="text-2xl mb-2 group-hover/feature:scale-125 transition-transform duration-300">
                    ⚡
                  </div>
                  <div className="text-sm text-gray-300">Instant Setup</div>
                </div>
                <div className="bg-gray-800/50 rounded-lg p-4 hover:bg-gray-700/50 transition-all duration-300 cursor-pointer group/feature">
                  <div className="text-2xl mb-2 group-hover/feature:scale-125 transition-transform duration-300">
                    🔧
                  </div>
                  <div className="text-sm text-gray-300">
                    Easy Customization
                  </div>
                </div>
                <div className="bg-gray-800/50 rounded-lg p-4 hover:bg-gray-700/50 transition-all duration-300 cursor-pointer group/feature">
                  <div className="text-2xl mb-2 group-hover/feature:scale-125 transition-transform duration-300">
                    🚀
                  </div>
                  <div className="text-sm text-gray-300">Deploy Anywhere</div>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-6 justify-center">
                <a
                  href="https://github.com/Vaibhav2154/PyEveryday"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group/btn px-10 py-5 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-2xl font-bold text-lg hover:shadow-lg hover:shadow-cyan-500/25 transition-all duration-300 hover:scale-105 relative overflow-hidden"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-purple-500 opacity-0 group-hover/btn:opacity-100 transition-opacity duration-300"></div>
                  <span className="relative flex items-center justify-center space-x-3">
                    <span>Deploy Scripts</span>
                    <svg
                      className="w-6 h-6 group-hover/btn:translate-x-2 transition-transform duration-300"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M13 7l5 5m0 0l-5 5m5-5H6"
                      />
                    </svg>
                  </span>
                </a>

                <button className="group/btn px-10 py-5 border-2 border-cyan-400 rounded-2xl font-bold text-lg text-cyan-400 hover:bg-cyan-400 hover:text-black transition-all duration-300 relative overflow-hidden">
                  <div className="absolute inset-0 bg-cyan-400 transform scale-x-0 group-hover/btn:scale-x-100 transition-transform duration-300 origin-left"></div>
                  <span className="relative">Explore Documentation</span>
                </button>
              </div>

              {/* Social proof indicators */}
              <div className="flex justify-center items-center space-x-8 mt-8 text-sm text-gray-400">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span>25+ Scripts Active</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div
                    className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"
                    style={{ animationDelay: "0.5s" }}
                  ></div>
                  <span>Open Source</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div
                    className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"
                    style={{ animationDelay: "1s" }}
                  ></div>
                  <span>MIT Licensed</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Enhanced Footer - Interactive */}
      <footer className="py-16 border-t border-gray-800 relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute bottom-0 left-0 w-full h-32 bg-gradient-to-t from-cyan-900/10 to-transparent"></div>
        </div>

        <div className="relative max-w-6xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center space-x-4 mb-8 group cursor-pointer">
            <div className="w-12 h-12 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-2xl flex items-center justify-center group-hover:rotate-12 group-hover:scale-110 transition-all duration-300 shadow-lg shadow-cyan-500/25">
              <span className="text-white font-bold text-xl">🐍</span>
            </div>
            <span className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent group-hover:scale-105 transition-transform duration-300">
              PyEveryday
            </span>
          </div>

          <p className="text-gray-400 mb-4 text-lg hover:text-gray-300 transition-colors duration-300 cursor-default">
            Automating the future, one Python script at a time.
          </p>

          <div className="flex justify-center space-x-8 mb-6">
            <a
              href="https://github.com/Vaibhav2154/PyEveryday"
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-2 text-gray-400 hover:text-cyan-400 transition-all duration-300 font-medium hover:scale-105 transform relative group"
            >
              <span className="relative z-10">GitHub Repository</span>
              <div className="absolute inset-0 bg-cyan-400/10 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-0"></div>
            </a>
            <button className="px-3 py-2 text-gray-400 hover:text-cyan-400 transition-all duration-300 font-medium hover:scale-105 transform relative group">
              <span className="relative z-10">Documentation</span>
              <div className="absolute inset-0 bg-cyan-400/10 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-0"></div>
            </button>
            <button className="px-3 py-2 text-gray-400 hover:text-cyan-400 transition-all duration-300 font-medium hover:scale-105 transform relative group">
              <span className="relative z-10">License</span>
              <div className="absolute inset-0 bg-cyan-400/10 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-0"></div>
            </button>
          </div>

          <div className="border-t border-gray-800 pt-8">
            <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
              <div className="text-gray-500 text-sm">
                © 2025 PyEveryday • Open Source • Built by Vaibhav2154
              </div>
              <div className="flex space-x-4">
                <div className="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center hover:bg-cyan-500 transition-all duration-300 cursor-pointer group">
                  <svg
                    className="w-4 h-4 text-gray-400 group-hover:text-white"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                  </svg>
                </div>
                <div className="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center hover:bg-purple-500 transition-all duration-300 cursor-pointer group">
                  <span className="text-gray-400 group-hover:text-white text-xs font-bold">
                    𝕏
                  </span>
                </div>
                <div className="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center hover:bg-blue-500 transition-all duration-300 cursor-pointer group">
                  <span className="text-gray-400 group-hover:text-white text-xs font-bold">
                    in
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
