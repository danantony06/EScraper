import { useState } from "react";
import { NavBar } from "@/components/NavBar";
import GridExample from "@/components/dataTable";
import CSLogo from "../assets/CS2Logo.png";
import playerLogo from "../assets/header_ctt.png";
import LeaugeLogo from "../assets/LuegeFinal.png";
import ValLogo from "../assets/VALor.png";
import DotaLogo from "../assets/Dota_2_Logo_processed.webp";
import { statType } from "@/constants";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { sportsBooks } from "@/constants";


export function ResearchPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedStat, setSelectedStat] = useState<string>(""); 
  const [selectedSportsbook, setSelectedSportsbook] = useState<string>("");

  const handleStatChange = (value: string) => {
    setSelectedStat(value);
  };
  
  const handleSportsbookChange = (value: string) => {
    setSelectedSportsbook(value);
  };
  
  const searchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  return (
    <div className="min-h-screen bg-[#0a0b1a]">
      <NavBar />
      
      <div className="container mx-auto">
        <div className="w-full border-b border-neutral-700/80 py-3">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex flex-wrap items-center gap-6">
              <button className="flex items-center hover:bg-orange-600 text-white h-12 font-extrabold py-2 px-4 rounded-lg transition-colors">
                <img src={playerLogo} alt="Shoota" className="h-6 mr-2" />
                ALL ESPORTS
              </button>

              <div className="flex items-center gap-4">
                <img
                  src={LeaugeLogo}
                  alt="League of Legends"
                  className="h-20 w-20 object-contain opacity-70 hover:opacity-100 transition"
                />
                <img
                  src={CSLogo}
                  alt="Counter Strike 2"
                  className="h-20 w-25 object-contain brightness-200 drop-shadow-lg hover:brightness-400 transition"
                />
                <img
                  src={ValLogo}
                  alt="VALORANT"
                  className="h-20 w-26 object-contain opacity-70 hover:opacity-100 transition"
                />
                <img
                  src={DotaLogo}
                  alt="Dota 2"
                  className="h-15 w-15 object-contain opacity-70 hover:opacity-100 transition"
                />
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-4">
              <Select onValueChange={handleStatChange}>
                <SelectTrigger className="w-[200px] inline-flex items-center gap-2 leading-[1] border whitespace-nowrap font-bold transition-colors disabled:pointer-events-none disabled:opacity-50 text-white uppercase bg-transparent hover:bg-[#2E3137]/30 py-[12px] rounded-[8px] border-[#2B365C] relative transition-all duration-300 hover:scale-105 z-10">
                  <SelectValue placeholder="Filter By Stat Type" />
                </SelectTrigger>
                <SelectContent className="border-[#2B365C] bg-[#1b1e2b] text-white inline-flex items-center gap-2 leading-[1] border whitespace-nowrap font-bold transition-colors disabled:pointer-events-none disabled:opacity-50 text-white uppercase bg-transparent hover:bg-[#2E3137]/30 py-[12px] rounded-[8px] border-[#2B365C] relative transition-all duration-300 hover:scale-105 z-10">
                  {statType.map((item, index) => (
                    <SelectItem key={index} value={item.label}>
                      {item.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Select onValueChange={handleSportsbookChange}>
                <SelectTrigger className="w-[200px] inline-flex items-center gap-2 leading-[1] border whitespace-nowrap font-bold transition-colors disabled:pointer-events-none disabled:opacity-50 text-white uppercase bg-transparent hover:bg-[#2E3137]/30 py-[12px] rounded-[8px] border-[#2B365C] relative transition-all duration-300 hover:scale-105 z-10">
                  <SelectValue placeholder="Filter By Sportsbook" />
                </SelectTrigger>
                <SelectContent className="border-[#2B365C] bg-[#1b1e2b] text-white inline-flex items-center gap-2 leading-[1] border whitespace-nowrap font-bold transition-colors disabled:pointer-events-none disabled:opacity-50 text-white uppercase bg-transparent hover:bg-[#2E3137]/30 py-[12px] rounded-[8px] border-[#2B365C] relative transition-all duration-300 hover:scale-105 z-10">
                  {sportsBooks.map((item, index) => (
                    <SelectItem key={index} value={item.label} className="flex items-center gap-2">
                      {item.label}
                      <img src={item.src} alt={item.label} className="h-5" />
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <div className="relative w-[250px]">
                <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                  <svg
                    className="w-4 h-4 text-purple-500"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 20 20"
                  >
                    <path
                      stroke="currentColor"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
                    />
                  </svg>
                </div>
                <input
                  type="search"
                  onChange={searchChange}
                  value={searchTerm}
                  className="block w-full p-3 ps-10 text-sm font-bold text-white border border-[#2B365C] rounded-lg bg-[#1b1e2b] focus:ring-orange-500 focus:border-orange-500 placeholder-gray-400 hover:bg-[#2E3137]/30 transition-all duration-300"
                  placeholder="Search by Player..."
                />
              </div>
            </div>
          </div>
        </div>
        <div className="w-full p-1">
          <div>
            <GridExample 
              selectedStat={selectedStat}
              searchTerm={searchTerm}
              selectedSportsbook={selectedSportsbook}
            />
          </div>
        </div>
      </div>
    </div>
  );
}