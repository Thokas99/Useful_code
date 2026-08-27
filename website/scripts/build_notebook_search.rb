#!/usr/bin/env ruby

require "json"
require "pathname"
require "yaml"

site_dir = Pathname.new(__dir__).parent
repo_dir = site_dir.parent
methods_file = site_dir.join("_data", "methods.yml")
output_file = site_dir.join("_data", "notebook_search.json")
catalog = {}
methods = YAML.load_file(methods_file)

methods.each do |family_key, family|
  family.fetch("notebooks").each do |notebook|
    path = notebook.fetch("path")
    abort "Duplicate catalog path: #{path}" if catalog.key?(path)

    catalog[path] = {
      "family" => family_key,
      "title" => notebook.fetch("title")
    }
  end
end

template_paths = Dir[repo_dir.join("templates/**/*.qmd").to_s].map do |path|
  Pathname.new(path).relative_path_from(repo_dir).to_s
end.sort
catalog_paths = catalog.keys.sort

unless template_paths == catalog_paths
  missing = template_paths - catalog_paths
  stale = catalog_paths - template_paths
  abort "Catalog mismatch; missing=#{missing.inspect} stale=#{stale.inspect}"
end

search_data = methods.each_key.to_h { |family_key| [family_key, []] }
template_paths.each do |path|
  notebook = catalog.fetch(path)
  source = File.read(repo_dir.join(path), encoding: "UTF-8")
  search_data.fetch(notebook.fetch("family")) << "#{notebook.fetch("title")}\n#{path}\n#{source}"
end

File.write(output_file, JSON.pretty_generate(search_data) + "\n")
puts "Indexed #{template_paths.length} notebooks for site search."
