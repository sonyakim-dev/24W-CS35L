#!/usr/local/cs/bin/python3
from collections import deque, defaultdict
import os
import sys
import zlib


class CommitNode:
  def __init__(self, commit_hash: str, branch_names: set[str] = None):
    self.commit_hash: str = commit_hash
    self.branch_names: set[str] = set(branch_names) if branch_names else set()
    self.parents: set[str] = set()  # store parent hashes
    self.children: set[str] = set()  # store child hashes


def get_git_directory() -> str:
  curr_path = os.getcwd()  # get a current directory

  while True:
    git_path = os.path.join(curr_path, '.git')

    # if .git exists in the current directory, return the directory
    if os.path.isdir(git_path):
      return git_path

    # if curr_dir reaches root, exit with 1
    if curr_path == '/':
      print('Not inside a Git repository', file=sys.stderr)
      sys.exit(1)

    # move up to the parent directory
    curr_path = os.path.dirname(curr_path)


def get_local_branches(git_path: str) -> dict[str, list[str]]:
  refs_path = os.path.join(git_path, 'refs', 'heads')
  branches: dict[str, list[str]] = {}  # key: commit_hash, value: list of branch_names

  # walking through the refs/heads directory tree
  for (root, _, files) in os.walk(refs_path):
    for file in files:
      # get the branch name relative to refs/heads
      branch_name = os.path.relpath(os.path.join(root, file), refs_path)
      with open(os.path.join(root, file), 'r') as f:
        commit_hash = f.read().strip()
        branches.setdefault(commit_hash, []).append(branch_name)

  return branches


def build_commit_graph(git_path: str, branches: dict[str, list[str]]) -> tuple[dict[str, CommitNode], set[str]]:
  commit_graph: dict[str, CommitNode] = {}
  root_hashes: set[str] = set()  # store root_hashes which doesn't have parents
  stack: list[str] = []  # dfs stack, store commit_hash

  for commit_hash, branch_names in branches.items():
    commit_node = CommitNode(commit_hash, branch_names)
    commit_graph[commit_hash] = commit_node
    stack.append(commit_hash)

  while stack:
    commit_hash = stack.pop()
    commit_node = commit_graph[commit_hash]

    # add the commit to the commit_nodes if it doesn't exist
    if commit_hash not in commit_graph:
      commit_graph[commit_hash] = CommitNode(commit_hash)

    parent_hashes = get_parent_hashes(git_path, commit_hash)

    if not parent_hashes:
      root_hashes.add(commit_hash)

    for parent_hash in parent_hashes:
      # add the parent commit to the commit_nodes if it doesn't exist
      if parent_hash not in commit_graph:
        commit_graph[parent_hash] = CommitNode(parent_hash)

      parent_node = commit_graph[parent_hash]
      commit_node.parents.add(parent_hash)
      parent_node.children.add(commit_hash)

      stack.append(parent_hash)

  return (commit_graph, root_hashes)


def get_parent_hashes(git_path: str, commit_hash: str) -> str:
  object_path = os.path.join(git_path, 'objects', commit_hash[:2], commit_hash[2:])

  with open(object_path, 'rb') as f:
    commit_content = zlib.decompress(f.read()).decode('utf-8')
    lines = commit_content.split('\n')
    return [line.split(' ')[1] for line in lines if line.startswith('parent')]


def get_topological_order(commit_graph: dict[str, CommitNode], root_hashes: set[str]) -> list[str]:
  topological_order: list[str] = []
  # kahn's algorithm: store in-degree of all commit_hash
  in_degree: dict[str, int] = defaultdict(int)
  # push root_hashes to deque which has no incoming edges
  queue = deque(root_hashes)
  visited_count = 0

  # compute in-degree of all nodes
  for commit_node in commit_graph.values():
    for child in commit_node.children:
      in_degree[child] += 1

  while queue:
    # pop front and add it to topological order
    commit_hash = queue.popleft()
    topological_order.append(commit_hash)
    visited_count += 1

    for child in commit_graph[commit_hash].children:
      in_degree[child] -= 1
      # if in-degree becomes zero, add it to queue
      if in_degree[child] == 0:
        queue.appendleft(child)

  # check if there is a cycle
  if visited_count != len(commit_graph):
    print('cycle exists in the graph')
    sys.exit(1)

  return topological_order[::-1]


def print_commit_hashes(ordered_commits: list[str], commit_graph: dict[str, CommitNode]) -> None:
  sticky_start = False

  for i, commit_hash in enumerate(ordered_commits):
    commit_node = commit_graph[commit_hash]

    # sticky start
    if sticky_start:
      print(f"={' '.join(commit_node.children)}")
      sticky_start = False

    print(f"{commit_hash} {' '.join(sorted(commit_node.branch_names))}", end='')

    # sticky end
    next_commit = ordered_commits[i+1] if i < len(ordered_commits)-1 else None
    if next_commit and (next_commit not in commit_node.parents):
      print(f"\n{' '.join(commit_node.parents)}=\n")
      sticky_start = True
    else:
      print()


def topo_order_commits():
  git_path = get_git_directory()
  branches = get_local_branches(git_path)
  commit_graph, root_hashes = build_commit_graph(git_path, branches)
  ordered_commits = get_topological_order(commit_graph, root_hashes)
  print_commit_hashes(ordered_commits, commit_graph)


if __name__ == '__main__':
  topo_order_commits()
