export interface Video {
  file: string; // public-rooted path (mp4)
  poster?: string; // public-rooted path (jpg)
  caption?: string;
  date?: string;
}

export const videos: Video[] = [
  { file: "/videos/img_0815.mp4", poster: "/videos/img_0815.jpg" },
  { file: "/videos/img_0828.mp4", poster: "/videos/img_0828.jpg" },
  { file: "/videos/img_6141.mp4", poster: "/videos/img_6141.jpg" },
  { file: "/videos/img_0633.mp4", poster: "/videos/img_0633.jpg" },
  { file: "/videos/untitled_project.mp4", poster: "/videos/untitled_project.jpg" },
  { file: "/videos/untitled_project2.mp4", poster: "/videos/untitled_project2.jpg" },
  { file: "/videos/untitled_project3.mp4", poster: "/videos/untitled_project3.jpg" },
  { file: "/videos/frequency_final1.mp4", poster: "/videos/frequency_final1.jpg" },
  { file: "/videos/mellownsimi_final1.mp4", poster: "/videos/mellownsimi_final1.jpg" },
];
