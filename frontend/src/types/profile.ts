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

<<<<<<< HEAD
=======
export interface CompanySummary {
  id: number;
  name: string;
  website?: string;
  location?: string;
}

>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
export interface RecruiterProfile {
  userId: number;
  name: string;
  email: string;
  phone?: string;
<<<<<<< HEAD
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
=======
  designation?: string;
  company?: CompanySummary | null;
}

export interface RecruiterProfileUpdateRequest {
  phone?: string;
  designation?: string;
  companyName?: string;
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
}
