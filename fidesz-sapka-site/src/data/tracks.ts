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
    date: "2025-07-10",
    audio: "/audio/ADIDEMASTER6.mp3",
    duration: "3:40",
  },
  {
    slug: "kia",
    title: "kia",
    date: "2025-08-14",
    audio: "/audio/KIAMASTER10.mp3",
    duration: "2:48",
  },
  {
    slug: "kiraly",
    title: "kiraly",
    date: "2026-03-19",
    audio: "/audio/kiralyM9.mp3",
    duration: "2:40",
  },
  {
    slug: "frequencyM11",
    title: "frequencyM11",
    date: "pending",
    audio: "",
    pending: true,
  },
];
