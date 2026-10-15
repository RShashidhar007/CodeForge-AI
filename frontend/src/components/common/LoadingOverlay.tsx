import { Spinner } from "./Spinner";

interface LoadingOverlayProps {
  message?: string;
}

export function LoadingOverlay({ message }: LoadingOverlayProps) {
  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: "1rem",
        zIndex: 1000,
      }}
    >
      <Spinner size={48} />
      {message && (
        <div style={{ color: "white", fontSize: "1rem" }}>
          {message}
        </div>
      )}
    </div>
  );
}
