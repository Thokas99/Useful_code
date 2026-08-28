#!/usr/bin/env ruby

require "fileutils"
require "tmpdir"
require "yaml"

site_dir = File.expand_path("..", __dir__)
repo_dir = File.expand_path("..", site_dir)
methods_file = File.join(site_dir, "_data", "methods.yml")
download_dir = File.join(site_dir, "downloads")

methods = YAML.load_file(methods_file)
FileUtils.rm_rf(download_dir)
FileUtils.mkdir_p(download_dir)

notebook_root = File.join(download_dir, "notebooks")
section_root = File.join(download_dir, "sections")
FileUtils.mkdir_p(notebook_root)
FileUtils.mkdir_p(section_root)

total_notebooks = 0

Dir.mktmpdir("useful-code-downloads-") do |staging_root|
  methods.each_value do |family|
    slug = family.fetch("slug")
    abort "Unsafe method-family slug: #{slug}" unless slug.match?(/\A[a-z0-9-]+\z/)

    notebook_dir = File.join(notebook_root, slug)
    staging_dir = File.join(staging_root, slug)
    FileUtils.mkdir_p(notebook_dir)
    FileUtils.mkdir_p(staging_dir)
    basenames = {}

    family.fetch("notebooks").each do |notebook|
      relative_path = notebook.fetch("path")
      source = File.expand_path(relative_path, repo_dir)
      expected_root = repo_dir + File::SEPARATOR
      abort "Notebook path escapes repository: #{relative_path}" unless source.start_with?(expected_root)
      abort "Notebook source does not exist: #{relative_path}" unless File.file?(source)
      abort "Not a QMD notebook: #{relative_path}" unless File.extname(source) == ".qmd"

      basename = File.basename(source)
      abort "Duplicate notebook basename in #{slug}: #{basename}" if basenames.key?(basename)

      FileUtils.cp(source, File.join(notebook_dir, basename))
      FileUtils.cp(source, File.join(staging_dir, basename))
      basenames[basename] = true
      total_notebooks += 1
    end

   zip_path = File.join(section_root, "#{slug}.zip")
   Dir.chdir(staging_root) do
      section_files = Dir[File.join(slug, "*.qmd")]
      abort "zip failed for #{slug}" unless system("zip", "-q", zip_path, *section_files)
   end
  end
end

puts "Generated #{total_notebooks} notebook downloads and #{methods.length} section ZIPs."
