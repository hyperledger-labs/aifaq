import type { Metadata } from "next"
import { Inter, Space_Grotesk } from "next/font/google"
import "./globals.css"
import { cn } from "@/lib/utils"
import Providers from "@/components/providers"

const fontPrimary = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-primary",
})

const fontSecondary = Inter({
  subsets: ["latin"],
  variable: "--font-secondary",
})

export const metadata: Metadata = {
  title: "AIFAQ",
  description: "",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={cn(
          "font-secondary antialiased",
          fontPrimary.variable,
          fontSecondary.variable
        )}>
        <div className="h-screen w-screen">
          <Providers>
            {children}
          </Providers>
        </div>
      </body>
    </html>
  );
}