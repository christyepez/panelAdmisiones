# v1.60.1 - Path resolution fix

Power Query no longer depends exclusively on `C:\Users\chris`.

Resolved folders:
- Current data: `Admisiones\Actual`
- Historical data: `Admisiones\Historicos`

Known Windows user roots checked automatically:
1. `C:\Users\ChristianYepez\...`
2. `C:\Users\chris\...`

No report visual, relationship, Oferta logic, or target measure was changed in this patch.
