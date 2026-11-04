@echo off
cd /d C:\tmp\opus55\recheck-02c-20261103\run
for %%s in (no_inverse_on_time_links wrong_plane wrong_multiplicity negative_weight_called_positive signed_site_weight_called_positive bad_projector no_inverse_in_gram wrong_plane_in_gram dropped_inverse_third_letter dropped_inverse_fourth_letter every_function_one_plane t4_half_weights_dropped no_such_name) do (
  start "" /belownormal /b /wait python3 -I -X utf8 t.py sabotage=%%s > ..\out\sab-%%s.out 2>&1
  echo SABOTAGE=%%s exit=!ERRORLEVEL!
)
