interface ProgressBarProps {
  percentage: number;
  showLabel?: boolean;
}

export function ProgressBar({ percentage, showLabel = false }: ProgressBarProps) {
  const clampedPercentage = Math.min(100, Math.max(0, percentage));

  return (
    <div style={{ width: "100%" }}>
      <div
        style={{
          width: "100%",
          height: "8px",
          backgroundColor: "var(--color-border)",
          borderRadius: "4px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${clampedPercentage}%`,
            height: "100%",
            backgroundColor: "var(--color-primary)",
            transition: "width 0.3s ease",
          }}
        />
      </div>
      {showLabel && (
        <div
          style={{
            fontSize: "0.85rem",
            color: "var(--color-muted)",
            marginTop: "0.25rem",
            textAlign: "center",
          }}
        >
          {clampedPercentage}%
        </div>
      )}
    </div>
  );
}
