export interface CandidateProfile {
  userId: number;
  name: string;
  email: string;
  phone?: string;
  location?: string;
  bio?: string;
  skills: string[];
  githubUrl?: string;
  linkedinUrl?: string;
}

export interface CandidateProfileUpdateRequest {
  phone?: string;
  location?: string;
  bio?: string;
  skills: string[];
  githubUrl?: string;
  linkedinUrl?: string;
}

export interface RecruiterProfile {
  userId: number;
  name: string;
  email: string;
  phone?: string;
  position?: string;
  bio?: string;
  companyId?: number | null;
  companyName?: string | null;
}

export interface RecruiterProfileUpdateRequest {
  name?: string;
  phone?: string;
  position?: string;
  bio?: string;
}
