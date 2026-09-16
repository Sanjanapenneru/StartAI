import { Link, Navigate } from "react-router-dom";
import { ArrowRight, Calculator, Clock3, IndianRupee } from "lucide-react";
import { useGramai } from "../context/GramaiContext";

const currency = (value) =>
  `₹${Number(value || 0).toLocaleString("en-IN", {
    maximumFractionDigits: 0,
  })}`;

function Stat({ label, value, accent = false }) {
  return (
    <div className={`rounded-2xl border p-5 ${accent ? "border-[#0c3b5e] bg-[#0c3b5e] text-white" : "border-slate-200 bg-white"}`}>
      <p className={`text-xs font-bold uppercase tracking-wider ${accent ? "text-blue-200" : "text-slate-400"}`}>{label}</p>
      <p className={`mt-3 text-2xl font-black ${accent ? "text-white" : "text-[#0c3b5e]"}`}>{value}</p>
    </div>
  );
}

export default function FinancePage() {
  const { assessment, result } = useGramai();
  if (!assessment || !result) return <Navigate to="/assessment" replace />;
  const plan = result.financial_plan || {};
  const repayment = plan.repayment || {};

  return (
    <div className="mx-auto max-w-7xl px-5 py-12 lg:px-8 lg:py-16">
      <p className="text-xs font-bold uppercase tracking-[0.18em] text-[#bc7b10]">Step 3 of 3 · Financial planner</p>
      <div className="mt-3 flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
        <div>
          <h1 className="text-4xl font-black tracking-tight text-[#0c3b5e]">Plan the financing before you borrow.</h1>
          <p className="mt-3 text-base text-slate-500">These values are calculated by deterministic backend rules.</p>
        </div>
        <div className="flex items-center gap-2 rounded-full bg-blue-50 px-4 py-2 text-sm font-extrabold text-[#0c3b5e]">
          <Calculator className="h-4 w-4" /> {plan.scheme || "Unsupported"}
        </div>
      </div>

      {!plan.supported ? (
        <div className="mt-10 rounded-2xl border border-red-200 bg-red-50 p-6 text-red-800">
          <h2 className="font-extrabold">Project exceeds the supported scheme limit.</h2>
          <p className="mt-2 text-sm">The calculated project cost is {currency(plan.project_cost)}. GRAMAI will not recommend an unsupported loan.</p>
        </div>
      ) : (
        <>
          <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Stat label="Available capital" value={currency(assessment.available_capital)} />
            <Stat label="Project cost" value={currency(plan.project_cost)} />
            <Stat label="Calculated financing" value={currency(plan.calculated_financing)} />
            <Stat label="Supported loan" value={currency(plan.supported_loan)} accent />
          </div>

          <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Stat label="Scheme maximum" value={currency(plan.scheme_maximum_loan)} />
            <Stat label="Interest" value={`${Number(plan.interest_rate * 100).toFixed(1)}% p.a.`} />
            <Stat label="Tenure" value={`${plan.tenure_years} years`} />
            <Stat label="Moratorium" value={`${plan.moratorium_months} months`} />
          </div>

          <div className="mt-8 grid gap-5 lg:grid-cols-[0.8fr_1.2fr]">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="rounded-xl bg-amber-50 p-3 text-[#bc7b10]"><IndianRupee className="h-5 w-5" /></div>
                <div>
                  <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Why this scheme?</p>
                  <h2 className="mt-1 text-xl font-black text-[#0c3b5e]">{plan.scheme}</h2>
                </div>
              </div>
              <p className="mt-6 text-sm leading-7 text-slate-600">{result.scheme_recommendation?.reason}</p>
              {plan.loan_gap > 0 && (
                <p className="mt-5 rounded-xl bg-amber-50 p-4 text-sm font-semibold leading-6 text-amber-800">
                  Your calculated financing is {currency(plan.loan_gap)} above the scheme maximum. The supported loan shown above is the capped amount.
                </p>
              )}
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Repayment planning</p>
                  <h2 className="mt-1 text-xl font-black text-[#0c3b5e]">Estimated quarterly schedule</h2>
                </div>
                <Clock3 className="h-5 w-5 text-[#0c3b5e]" />
              </div>
              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                <div className="rounded-xl bg-blue-50 p-4">
                  <p className="text-xs font-bold uppercase tracking-wider text-[#0c3b5e]">Quarterly payment</p>
                  <p className="mt-2 text-xl font-black text-[#0c3b5e]">{currency(repayment.estimated_quarterly_payment)}</p>
                </div>
                <div className="rounded-xl bg-slate-50 p-4">
                  <p className="text-xs font-bold uppercase tracking-wider text-slate-500">Illustrative Monthly EMI</p>
                  <p className="mt-2 text-xl font-black text-slate-700">{currency(repayment.illustrative_monthly_emi)}</p>
                </div>
              </div>
              <p className="mt-5 text-xs leading-5 text-slate-500">The monthly EMI is for easier understanding only. It is not the official quarterly repayment schedule.</p>
            </div>
          </div>

          <div className="mt-6 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
            <div className="border-b border-slate-100 px-5 py-4">
              <h3 className="font-extrabold text-slate-800">First repayment quarters</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full min-w-[600px] text-left text-sm">
                <thead className="bg-slate-50 text-xs uppercase tracking-wider text-slate-400">
                  <tr><th className="px-5 py-3">Installment</th><th className="px-5 py-3">Due after</th><th className="px-5 py-3">Principal</th><th className="px-5 py-3">Interest</th><th className="px-5 py-3">Payment</th></tr>
                </thead>
                <tbody>
                  {(repayment.quarterly_schedule || []).slice(0, 6).map((row) => (
                    <tr key={row.installment} className="border-t border-slate-100 text-slate-600">
                      <td className="px-5 py-3 font-bold text-slate-800">{row.installment}</td>
                      <td className="px-5 py-3">{row.due_after_months} months</td>
                      <td className="px-5 py-3">{currency(row.principal)}</td>
                      <td className="px-5 py-3">{currency(row.interest)}</td>
                      <td className="px-5 py-3 font-bold">{currency(row.payment)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      <div className="mt-8 flex justify-end">
        <Link to="/recommendation" className="inline-flex items-center gap-2 rounded-xl bg-[#0c3b5e] px-5 py-3.5 text-sm font-extrabold text-white hover:bg-[#092d47]">
          View final recommendation <ArrowRight className="h-4 w-4" />
        </Link>
      </div>
    </div>
  );
}