import { Message } from "@/lib/types";

export default function ChatResponse({ content }: Message) {
    return (
        <div className='flex w-full bg-background'>
            <p>{content}</p>
        </div>
    )
}