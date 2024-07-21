import Sidebar from "@/components/sidebar";
import ChatHeader from "@/components/chat-header";
import WelcomeSection from "@/components/welcome-section";
import ChatSection from "@/components/chat-section";

export default function Home() {
  const chatSelected = false;
  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex flex-col flex-1">
        <ChatHeader />
        <div className="flex-1 overflow-y-auto bg-background">
          {chatSelected ? <WelcomeSection /> : <ChatSection />}
        </div>
      </main>
    </div>
  );
}
