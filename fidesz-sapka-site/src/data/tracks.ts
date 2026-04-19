export interface Track {
  slug: string;
  title: string;
  date: string; // YYYY-MM-DD, or YYYY-XX-XX if unknown
  audio: string; // public-rooted path
  duration?: string; // mm:ss
  credits?: string;
  lyric?: string;
  cover?: string;
  pending?: boolean;
}

export const tracks: Track[] = [
  {
    slug: "adide",
    title: "adide",
    date: "2025-XX-XX",
    audio: "/audio/adide.mp3",
    duration: "3:40",
  },
  {
    slug: "kia",
    title: "kia",
    date: "2025-XX-XX",
    audio: "/audio/kia.mp3",
    duration: "2:48",
  },
  {
    slug: "kiraly",
    title: "kiraly",
    date: "2026-04-XX",
    audio: "/audio/kiraly.mp3",
    duration: "2:40",
  },
  {
    slug: "pending",
    title: "—",
    date: "pending",
    audio: "",
    pending: true,
  },
];
