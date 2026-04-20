export interface Photo {
  file: string; // public-rooted path
  caption?: string;
  date?: string; // YYYY-MM-DD
}

// Captions default to the filename when empty. Fill in later.
export const photos: Photo[] = [
  { file: "/photos/dscf3751.jpg" },
  { file: "/photos/dsc_0745.jpg" },
  { file: "/photos/dsc_0750.jpg" },
  { file: "/photos/dsc_0787.jpg" },
  { file: "/photos/dsc_0807.jpg" },
  { file: "/photos/img_0306.jpg" },
  { file: "/photos/img_0351.jpg" },
  { file: "/photos/img_0354.jpg" },
  { file: "/photos/img_0266.jpg" },
  { file: "/photos/img_0308.jpg" },
  { file: "/photos/img_0377.jpg" },
  { file: "/photos/img_0410.jpg" },
  { file: "/photos/img_0486.jpg" },
  { file: "/photos/img_0489.jpg" },
  { file: "/photos/img_0620.jpg" },
  { file: "/photos/img_0632.jpg" },
  { file: "/photos/img_0651.jpg" },
  { file: "/photos/img_1782.jpg" },
];
