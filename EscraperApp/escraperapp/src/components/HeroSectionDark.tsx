import * as React from "react"
import { cn } from "@/lib/utils"
import { ChevronRight } from "lucide-react"

interface HeroSectionProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string
  subtitle?: {
    regular: string
    gradient: string
  }
  description?: string
  ctaText?: string
  ctaHref?: string
  gridOptions?: {
    angle?: number
    cellSize?: number
    opacity?: number
    lightLineColor?: string
    darkLineColor?: string
  }
}

const RetroGrid = ({
  angle = 65,
  cellSize = 60,
  opacity = 0.15, // Reduced opacity for deep dark theme
  lightLineColor = "rgba(75, 85, 175, 0.3)", // Blue-ish line color
  darkLineColor = "rgba(75, 85, 175, 0.3)", // Same for dark mode
}) => {
  const gridStyles = {
    "--grid-angle": `${angle}deg`,
    "--cell-size": `${cellSize}px`,
    "--opacity": opacity,
    "--light-line": lightLineColor,
    "--dark-line": darkLineColor,
  } as React.CSSProperties

  return (
    <div
      className={cn(
        "pointer-events-none fixed inset-0 size-full overflow-hidden [perspective:300px]",
        `opacity-[var(--opacity)]`,
      )}
      style={gridStyles}
    >
      <div className="absolute inset-0 [transform:rotateX(var(--grid-angle))]">
        <div className="animate-grid [background-image:linear-gradient(to_right,var(--light-line)_1px,transparent_0),linear-gradient(to_bottom,var(--light-line)_1px,transparent_0)] [background-repeat:repeat] [background-size:var(--cell-size)_var(--cell-size)] [height:300vh] [inset:0%_0px] [margin-left:-200%] [transform-origin:100%_0_0] [width:600vw] dark:[background-image:linear-gradient(to_right,var(--dark-line)_1px,transparent_0),linear-gradient(to_bottom,var(--dark-line)_1px,transparent_0)]" />
      </div>
      <div className="absolute inset-0 bg-gradient-to-t from-black via-black/90 to-transparent to-90%" />
    </div>
  )
}

const HeroSectionDark = React.forwardRef<HTMLDivElement, HeroSectionProps>(
  (
    {
      className,
      title = "Build products for everyone",
      subtitle = {
        regular: "Designing your projects faster with ",
        gradient: "the largest figma UI kit.",
      },
      description = "Sed ut perspiciatis unde omnis iste natus voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae.",
      ctaText = "Browse courses",
      ctaHref = "#",
      gridOptions,
      ...props
    },
    ref,
  ) => {
    return (
      <div 
        className={cn("relative w-full h-screen overflow-hidden bg-[#0a0b1a]", className)} 
        ref={ref} 
        {...props}
      >
        {/* Deep dark background with gradient overlays */}
        <div className="fixed inset-0 z-0 bg-[#0a0b1a] bg-[radial-gradient(ellipse_70%_50%_at_50%_-10%,rgba(54,40,114,0.15),rgba(10,11,26,0))]" />
        
        {/* Glowing accent elements */}
        <div className="fixed -left-20 top-20 h-64 w-64 rounded-full bg-indigo-900/20 blur-3xl animate-pulse" style={{ animationDuration: "7s" }} />
        <div className="fixed right-0 top-1/3 h-72 w-72 rounded-full bg-purple-700/10 blur-3xl animate-pulse" style={{ animationDuration: "8s", animationDelay: "1s" }} />
        <div className="fixed left-1/4 bottom-0 h-80 w-80 rounded-full bg-blue-700/10 blur-3xl animate-pulse" style={{ animationDuration: "9s", animationDelay: "2s" }} />
        
        {/* Subtle color streaks */}
        <div className="fixed top-0 left-1/4 w-1 h-screen bg-gradient-to-b from-blue-500/0 via-blue-500/10 to-blue-500/0 blur-xl" />
        <div className="fixed top-0 right-1/3 w-1 h-screen bg-gradient-to-b from-purple-500/0 via-purple-500/10 to-purple-500/0 blur-xl" />
        
        {/* Retro grid */}
        <RetroGrid {...gridOptions} />
        
        {/* Main content section */}
        <div className="relative z-10 w-full h-full flex items-center justify-center">
          <div className="w-full max-w-screen-xl px-4 md:px-8">
            <div className="space-y-8 max-w-3xl mx-auto text-center">
              {/* Badge with neon-like effect */}
              <h1 className="text-sm text-[#94a4ff] group font-medium mx-auto px-5 py-2 bg-[#192053]/40 backdrop-blur-sm border border-[#394198]/30 rounded-full w-fit transition-all duration-300 hover:border-[#394198]/60">
                {title}
                <ChevronRight className="inline w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform duration-300 ease-out" />
              </h1>
              
              {/* Bold heading with vibrant gradient */}
              <h2 className="text-5xl font-bold tracking-tight text-white mx-auto md:text-7xl">
  {subtitle.regular}
  <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#4f6bff] via-[#b955ff] to-[#4fb8ff] px-4">
    {subtitle.gradient}
  </span>
</h2>
              
              {/* Description with light blue tint */}
              <p className="max-w-2xl mx-auto text-[#a3b1e6] text-lg md:text-xl">
                {description}
              </p>
              
              {/* Vibrant CTA button with glow effect */}
              <div className="flex items-center justify-center mt-12">
                <div className="relative group">
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-[#4f6bff] to-[#b955ff] rounded-md blur-sm opacity-70 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
                  <a
                    href={ctaHref}
                    className="relative flex items-center justify-center px-10 py-4 bg-[#0f1029] rounded-md leading-none text-white font-medium transition-all duration-300 hover:scale-105 border border-[#394198]/30 group-hover:border-[#394198]/0"
                  >
                    <span className="absolute inset-0 rounded-md bg-gradient-to-r from-[#4f6bff]/10 to-[#b955ff]/10 blur-sm"></span>
                    <span className="relative z-10">{ctaText}</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  },
)
HeroSectionDark.displayName = "HeroSection"

export { HeroSectionDark }