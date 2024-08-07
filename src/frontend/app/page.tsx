import Sidebar from "@/components/sidebar";
import ChatPage from '@/components/chat-page';

export default function Home() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <ChatPage />
    </div>
  );
}
