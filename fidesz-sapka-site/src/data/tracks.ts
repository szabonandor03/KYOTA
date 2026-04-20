export interface Track {
  slug: string;
  title: string;
  date: string;
  audio: string;
  duration?: string;
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
    slug: "frequency",
    title: "frequency",
    date: "pending",
    audio: "",
    pending: true,
  },
];
