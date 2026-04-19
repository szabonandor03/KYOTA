export interface Video {
  file: string; // public-rooted path (mp4)
  poster?: string; // public-rooted path (jpg)
  caption?: string;
  date?: string;
}

// Phase 0: raw ambient clips only. Polished edits are stashed in /videos-archive/
// (see /public/videos-archive/) and can be surfaced later.
export const videos: Video[] = [
  { file: "/videos/img_0815.mp4", poster: "/videos/img_0815.jpg" },
  { file: "/videos/img_0828.mp4", poster: "/videos/img_0828.jpg" },
  { file: "/videos/img_6141.mp4", poster: "/videos/img_6141.jpg" },
];
