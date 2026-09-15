# Navigable dashboard

## Default view

The dashboard opens with `Grado con meta B26`, the only universe that can be compared directly with the adjusted institutional target of 2,400.

`Todos los programas` combines target-covered programs with programs that have no target, so target-dependent indicators are intentionally blank. `Programas sin meta` exposes the excluded population for review.

## Period logic

- B25: May 1, 2025 through September 30, 2025.
- B26: May 1, 2026 through September 30, 2026.
- Current B26 cutoff: September 15, 2026.
- Same-day comparison: day 138 of both periods.
- Linear projection: B26 actual / elapsed days × total period days.

Dates remain editable in the interface. The cutoff cannot exceed the source snapshot.

## Privacy

The extraction script reads identifiers only to count duplicates. The generated web dataset contains aggregated counts by period, campus, career, modality, date and formalization status. It does not contain student-level identifiers or contact fields.

## Known limitations

- The B26 business grain remains the candidate rule `B26 + HOMOLOGA=NO + MATRÍCULA EN PRIMERO=SI`.
- Formalization can be filtered but is not part of the default grain.
- Campus targets display only values that can be assigned from explicit `AMB`, `UIO` or `LTG` labels in `Metas.xlsx`.
- Rows without an identifiable campus target remain unallocated.
