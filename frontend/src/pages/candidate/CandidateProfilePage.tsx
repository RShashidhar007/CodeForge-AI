import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { candidateService } from "../../services/candidateService";
import { extractErrorMessage } from "../../services/apiClient";
import { Alert } from "../../components/Alert";
import { LoadingState } from "../../components/LoadingState";
import type { CandidateProfile } from "../../types/profile";

export function CandidateProfilePage() {
  const [profile, setProfile] = useState<CandidateProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const [phone, setPhone] = useState("");
  const [location, setLocation] = useState("");
  const [bio, setBio] = useState("");
  const [skillsText, setSkillsText] = useState("");
  const [githubUrl, setGithubUrl] = useState("");
  const [linkedinUrl, setLinkedinUrl] = useState("");

  useEffect(() => {
    candidateService
      .getMyProfile()
      .then((data) => {
        setProfile(data);
        setPhone(data.phone ?? "");
        setLocation(data.location ?? "");
        setBio(data.bio ?? "");
        setSkillsText(data.skills.join(", "));
        setGithubUrl(data.githubUrl ?? "");
        setLinkedinUrl(data.linkedinUrl ?? "");
      })
      .catch((err) => setError(extractErrorMessage(err)))
      .finally(() => setIsLoading(false));
  }, []);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setIsSaving(true);
    try {
      const skills = skillsText
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);

      const updated = await candidateService.updateMyProfile({
        phone,
        location,
        bio,
        skills,
        githubUrl,
        linkedinUrl,
      });
      setProfile(updated);
      setSuccess("Profile updated successfully.");
    } catch (err) {
      setError(extractErrorMessage(err));
    } finally {
      setIsSaving(false);
    }
  }

  if (isLoading) return <LoadingState label="Loading your profile..." />;

  return (
    <div>
      <h1>My Profile</h1>

      {error && <Alert type="error" message={error} />}
      {success && <Alert type="success" message={success} />}

      <div className="card">
        <h2>Account</h2>
        <p>
          <strong>{profile?.name}</strong>
          <br />
          {profile?.email}
        </p>
        {profile && profile.skills.length > 0 && (
          <div className="skills-list">
            {profile.skills.map((skill) => (
              <span className="skill-chip" key={skill}>
                {skill}
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="card">
        <h2>Edit profile</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="phone">Phone</label>
            <input id="phone" value={phone} onChange={(e) => setPhone(e.target.value)} />
          </div>
          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input id="location" value={location} onChange={(e) => setLocation(e.target.value)} />
          </div>
          <div className="form-group">
            <label htmlFor="bio">Bio</label>
            <textarea id="bio" rows={4} value={bio} onChange={(e) => setBio(e.target.value)} />
          </div>
          <div className="form-group">
            <label htmlFor="skills">Skills (comma-separated)</label>
            <input
              id="skills"
              value={skillsText}
              onChange={(e) => setSkillsText(e.target.value)}
              placeholder="Java, Spring Boot, React"
            />
          </div>
          <div className="form-group">
            <label htmlFor="githubUrl">GitHub URL</label>
            <input id="githubUrl" value={githubUrl} onChange={(e) => setGithubUrl(e.target.value)} placeholder="https://github.com/you" />
          </div>
          <div className="form-group">
            <label htmlFor="linkedinUrl">LinkedIn URL</label>
            <input
              id="linkedinUrl"
              value={linkedinUrl}
              onChange={(e) => setLinkedinUrl(e.target.value)}
              placeholder="https://linkedin.com/in/you"
            />
          </div>
          <button className="btn btn-primary" type="submit" disabled={isSaving}>
            {isSaving ? "Saving..." : "Save changes"}
          </button>
        </form>
      </div>
    </div>
  );
}
