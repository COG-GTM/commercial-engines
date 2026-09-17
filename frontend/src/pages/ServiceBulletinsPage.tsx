import { api } from "../api";
import { useApi } from "../useApi";

export function ServiceBulletinsPage() {
  const { data, error, loading } = useApi(() => api.serviceBulletins());
  if (loading) return <p className="muted">Loading service bulletins…</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <section>
      <div className="page-head">
        <h1>Service Bulletins</h1>
      </div>
      <table>
        <thead>
          <tr>
            <th>Number</th>
            <th>Title</th>
            <th>Family</th>
            <th>Category</th>
            <th>Status</th>
            <th>Related AD</th>
            <th className="num">Deadline (cyc)</th>
          </tr>
        </thead>
        <tbody>
          {(data ?? []).map((s) => (
            <tr key={s.id}>
              <td>{s.sbNumber}</td>
              <td>{s.title}</td>
              <td>{s.family}</td>
              <td>
                <span className={`chip cat-${s.category.toLowerCase()}`}>{s.category}</span>
              </td>
              <td>{s.status}</td>
              <td>{s.relatedAdNumber ?? "—"}</td>
              <td className="num">{s.complianceDeadlineCycles?.toLocaleString() ?? "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
