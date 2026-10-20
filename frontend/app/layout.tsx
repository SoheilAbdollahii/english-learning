import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "LingoPath — English learning", description: "Practice English writing and learn from clear feedback." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="fa" dir="rtl"><body>{children}</body></html>; }
