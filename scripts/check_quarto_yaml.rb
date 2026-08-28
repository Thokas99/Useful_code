#!/usr/bin/env ruby
# frozen_string_literal: true

require "yaml"
require "shellwords"

root = File.expand_path("..", __dir__)
files = `git -C #{Shellwords.escape(root)} ls-files -z`.split("\0").reject(&:empty?)
errors = []
checked = 0

files.each do |relative|
  path = File.join(root, relative)
  text = File.read(path)
  yaml_text = if relative.end_with?(".yml", ".yaml")
                text
              elsif relative.end_with?(".qmd") && text.start_with?("---\n")
                closing = text.index("\n---", 4)
                unless closing
                  errors << "#{relative}: missing closing front matter delimiter"
                  next
                end
                text[4...closing]
              end
  next unless yaml_text

  begin
    YAML.parse(yaml_text)
    checked += 1
  rescue Psych::Exception => error
    errors << "#{relative}: #{error.message.lines.first.strip}"
  end
end

if errors.empty?
  puts "YAML/Quarto front matter checks passed: #{checked} files"
  exit 0
end

warn errors.map { |error| "ERROR: #{error}" }
exit 1
