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

export interface CompanySummary {
  id: number;
  name: string;
  website?: string;
  location?: string;
}

export interface RecruiterProfile {
  userId: number;
  name: string;
  email: string;
  phone?: string;
  designation?: string;
  company?: CompanySummary | null;
}

export interface RecruiterProfileUpdateRequest {
  phone?: string;
  designation?: string;
  companyName?: string;
}
