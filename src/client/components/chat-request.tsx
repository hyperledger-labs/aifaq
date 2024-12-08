import { Message } from "@/lib/types";

export default function ChatRequest({ content }: Message) {
    return (
        <div className='flex w-full justify-end bg-background'>
            <p>{content}</p>
        </div>
    )
}