import { HeroSectionDark } from "@/components/HeroSectionDark";
import { NavBar } from "@/components/NavBar";
const HeroPage = () => {
  return (
    <>
    <NavBar/>
      <HeroSectionDark
        title="Welcome to a new era of E-Sports Betting"
        subtitle={{
          regular: "A new era of E-Sports Betting:",
          gradient: "ReadyUp.gg"
        }}
        description="Bet on your favorite sports with Peer to Peer lines, Crytpto transactionss and enhanced player research tools."
        ctaText="Start Betting"
        ctaHref="#"
        // bottomImage={{
        //   light: "https://example.com/light-image.png",
        //   dark: "https://example.com/dark-image.png",
        // }}
        gridOptions={{
          angle: 45,
          cellSize: 50,
          opacity: 0.3,
          lightLineColor: "#4a4a4a",
          darkLineColor: "2a2a2a"
        }}
      />
      </>
      
  );
}

export default HeroPage;
