"use client";
import ChatSection from "@/components/chat-section";
import { Textarea } from "@/components/ui/textarea";

export default function Home() {
  return (
    <main className="fixed h-full w-full bg-muted">
      <ChatSection />
    </main>
  );
}
