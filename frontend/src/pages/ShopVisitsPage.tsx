import { api } from "../api";
import { useApi } from "../useApi";

export function ShopVisitsPage() {
  const { data, error, loading } = useApi(() => api.shopVisits());
  if (loading) return <p className="muted">Loading shop visits…</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <section>
      <div className="page-head">
        <h1>Shop Visits</h1>
      </div>
      <table>
        <thead>
          <tr>
            <th>Engine</th>
            <th>Shop</th>
            <th>Workscope</th>
            <th>Inducted</th>
            <th>Status</th>
            <th>Released</th>
          </tr>
        </thead>
        <tbody>
          {(data ?? []).map((v) => (
            <tr key={v.id}>
              <td>{v.engineSerial}</td>
              <td>{v.shop}</td>
              <td>{v.workscope}</td>
              <td>{v.inductedOn}</td>
              <td>{v.status}</td>
              <td>
                {v.status === "RELEASED"
                  ? `${v.releasedBy ?? "—"} · ${v.releasedAt?.slice(0, 10) ?? ""}`
                  : "—"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
