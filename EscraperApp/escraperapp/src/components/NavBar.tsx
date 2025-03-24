import React from "react";
import Logo from "../assets/finalLogo.png";
import { NavBarItems } from "@/constants";
import { NavBarSign } from "@/constants";
import { Button } from "@/components/ui/button"

function NavBar() {
  return (
    <nav className="sticky top-0 z-50 w-full h-20 bg-[#0a0b1a] border-b border-neutral-700/80">
      <div className="w-full h-full flex justify-between items-center px-4">
        {/* Logo container */}
        <div className="h-full flex items-center">
          <img src={Logo} alt="Logo" className="h-full object-contain" />
        </div>
        
        {/* Navigation items */}
        <div className="flex items-center flex-grow justify-center"> 
          <ul className="flex space-x-6">
            {NavBarItems.map((item, index) => (
              <li key={index}>
                <a 
                  href={item.href} 
                  className="transition-colors font-extrabold text-[18px] uppercase font-blenderpro text-white hover:text-white/80"
                >
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </div>
        
        {/* Sign buttons */}
        <div className="flex items-center">
          <ul className="flex space-x-4">
          {NavBarSign.map((item, index) => (
          <li key={index} className="relative group">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-[#4f6bff]/40 to-[#b955ff]/40 rounded-md blur-sm opacity-0 group-hover:opacity-100 transition duration-300"></div>
                    <button className="w-full inline-flex items-center gap-2 leading-[1] border whitespace-nowrap font-bold transition-colors disabled:pointer-events-none disabled:opacity-50 text-white uppercase bg-transparent hover:bg-[#2E3137]/30 py-[12px] px-[30px] rounded-[8px] border-[#2B365C] relative transition-all duration-300 hover:scale-105 z-10">
                  {item.label}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </nav>
  );
}

export { NavBar };