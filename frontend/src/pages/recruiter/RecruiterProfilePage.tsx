import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { recruiterService } from "../../services/recruiterService";
import { extractErrorMessage } from "../../services/apiClient";
import { Alert } from "../../components/Alert";
import { LoadingState } from "../../components/LoadingState";
import type { RecruiterProfile } from "../../types/profile";

export function RecruiterProfilePage() {
  const [profile, setProfile] = useState<RecruiterProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const [phone, setPhone] = useState("");
  const [position, setPosition] = useState("");
  const [bio, setBio] = useState("");

  useEffect(() => {
    recruiterService
      .getMyProfile()
      .then((data) => {
        setProfile(data);
        setPhone(data.phone ?? "");
        setPosition(data.position ?? "");
        setBio(data.bio ?? "");
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
      const updated = await recruiterService.updateMyProfile({ phone, position, bio });
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
      </div>

      <div className="card">
        <h2>Company</h2>
        {profile?.companyName ? (
          <p>
            <strong>{profile.companyName}</strong>
          </p>
        ) : (
          <p className="form-hint">No company linked to this account yet.</p>
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
            <label htmlFor="position">Position</label>
            <input id="position" value={position} onChange={(e) => setPosition(e.target.value)} />
          </div>
          <div className="form-group">
            <label htmlFor="bio">Bio</label>
            <textarea id="bio" rows={3} value={bio} onChange={(e) => setBio(e.target.value)} />
          </div>
          <button className="btn btn-primary" type="submit" disabled={isSaving}>
            {isSaving ? "Saving..." : "Save changes"}
          </button>
        </form>
      </div>
    </div>
  );
}
