import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { CheckCircle, XCircle } from "lucide-react";
import { LoadingOverlay } from "../../components/common/LoadingOverlay";
import { githubService } from "../../services/api/githubService";
import { parseGithubError } from "../../utils/errorHandler";

export function GithubCallbackPage() {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const code = searchParams.get("code");
    const state = searchParams.get("state");

    if (!code || !state) {
      setStatus("error");
      setMessage("Missing authorization code or state");
      if (window.opener) {
        window.opener.postMessage(
          { type: "github-oauth-error", error: "Missing authorization code or state" },
          "*"
        );
      }
      return;
    }

    githubService
      .handleOAuthCallback(code, state)
      .then(() => {
        setStatus("success");
        setMessage("GitHub Connected!");
        if (window.opener) {
          window.opener.postMessage({ type: "github-oauth-success" }, "*");
        }
        setTimeout(() => {
          window.close();
        }, 1000);
      })
      .catch((err) => {
        const errorMessage = parseGithubError(err);
        setStatus("error");
        setMessage(errorMessage);
        if (window.opener) {
          window.opener.postMessage({ type: "github-oauth-error", error: errorMessage }, "*");
        }
      });
  }, [searchParams]);

  if (status === "loading") {
    return <LoadingOverlay message="Connecting to GitHub..." />;
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        padding: "2rem",
        textAlign: "center",
      }}
    >
      {status === "success" ? (
        <>
          <CheckCircle size={64} color="var(--color-success)" />
          <h1 style={{ marginTop: "1rem" }}>{message}</h1>
          <p style={{ color: "var(--color-muted)" }}>This window will close automatically...</p>
        </>
      ) : (
        <>
          <XCircle size={64} color="var(--color-error)" />
          <h1 style={{ marginTop: "1rem" }}>Connection Failed</h1>
          <p style={{ color: "var(--color-muted)", marginBottom: "1rem" }}>{message}</p>
          <button className="btn btn-primary" onClick={() => window.close()}>
            Close Window
          </button>
        </>
      )}
    </div>
  );
}
