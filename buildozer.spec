- name: Create .buildozer directory
  run: |
    mkdir -p .buildozer
    touch .buildozer/.gitkeep

- name: Build with Buildozer
  uses: ArtemSBulgakov/buildozer-action@v1
  id: buildozer
  with:
    workdir: .
    buildozer_version: stable
    command: buildozer -v android debug

- name: List .buildozer contents
  if: always()
  run: |
    echo "Contents of .buildozer directory:"
    ls -R .buildozer

- name: Upload buildozer.log
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: buildozer.log
    path: .buildozer/buildozer.log
