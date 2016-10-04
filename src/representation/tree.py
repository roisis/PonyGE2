from algorithm.parameters import params
from random import choice, randrange


class Tree:

    def __init__(self, expr, parent, max_depth=20, depth_limit=20):
        self.parent = parent
        self.max_depth = max_depth
        self.codon = None
        self.depth_limit = depth_limit
        self.id = None
        self.depth = 1
        self.root = expr
        self.children = []

    def __str__(self):
        result = "("
        result += str(self.root)
        for child in self.children:
            if len(child.children) > 0:
                result += " " + str(child)
            else:
                result += " " + str(child.root)
        result += ")"
        return result

    def __copy__(self):
        """
        Creates a new unique copy of self.
        
        :return: A new unique copy of self.
        """

        tree_copy = Tree(self.root, self.parent, self.max_depth,
                         self.depth_limit)
        tree_copy.codon, tree_copy.id = self.codon, self.id
        tree_copy.depth = self.depth
                
        for child in self.children:
            new_child = child.__copy__()
            new_child.parent = tree_copy
            tree_copy.children.append(new_child)

        return tree_copy

    def get_current_depth(self):
        """Get the depth of the current node."""

        count = 1
        current_parent = self.parent
        while current_parent is not None:
            count += 1
            current_parent = current_parent.parent
        return count

    def get_max_tree_depth(self, current, max_d=1):
        """ Returns the maximum depth of the tree from the current node. """

        curr_depth = current.get_current_depth()
        if curr_depth > max_d:
            max_d = curr_depth
        for child in current.children:
            max_d = child.get_max_tree_depth(child, max_d)
        return max_d

    def get_tree_info(self, current, number=0, max_depth=0):
        """ Get the number of nodes and the max depth of the tree.
        """

        number += 1
        if current.root in params['BNF_GRAMMAR'].non_terminals:
            current.id = number
            if current.parent:
                current.depth = current.parent.depth + 1
            else:
                current.depth = 1
            if current.depth > max_depth:
                max_depth = current.depth
            NT_kids = [kid for kid in
                       self.children if kid.root in
                       params['BNF_GRAMMAR'].non_terminals]
            if not NT_kids:
                number += 1
            else:
                for child in NT_kids:
                    max_depth, number = child.get_tree_info(child,
                                                            number,
                                                            max_depth)

        return max_depth, number

    def get_target_nodes(self, array, target=None):
        """
        Returns the all NT nodes which match the target NT list in a
        given tree.
        
        :param array: The array of all nodes that match the target.
        :param target: The target nodes to match.
        :return: The array of all nodes that match the target.
        """

        if self.root in params['BNF_GRAMMAR'].non_terminals:
            # Check if the current node is a non-terminal.
            
            if self.root in target:
                # Check if the current node matches the target.
                array.append(self)
            
            # Find all non-terminal children of the current node.
            NT_kids = [kid for kid in self.children if kid.root in
                       params['BNF_GRAMMAR'].non_terminals]
            
            for child in NT_kids:
                if NT_kids:
                    # Recursively call function on any non-terminal children.
                    array = child.get_target_nodes(array, target=target)
        
        return array

    def get_output(self):
        """
        Calls the recursive build_output(self) which returns a list of all
        node roots. Joins this list to create the full phenotype of an
        individual. This two-step process speeds things up as it only joins
        the phenotype together once rather than at every node.
        
        :return: The complete built phenotype string of an individual.
        """

        def build_output(tree):
            """
            Recursively adds all node roots to a list which can be joined to
            create the phenotype.

            :return: The list of all node roots.
            """
            
            output = []
            for child in tree.children:
                if not child.children:
                    # If the current child has no children it is a terminal.
                    # Append it to the output.
                    output.append(child.root)
                
                else:
                    # Otherwise it is a non-terminal. Recurse on all
                    # non-terminals.
                    output += build_output(child)

            return output
        
        return "".join(build_output(self))

    def get_labels(self, labels):
        """
        Recurses through a tree and appends all node roots to a set.
        
        :param labels: The set of roots of all nodes in the tree.
        :return: The set of roots of all nodes in the tree.
        """
        
        # Add the current root to the set of all labels.
        labels.add(self.root)

        for child in self.children:
            # Recurse on all children.
            
            labels = child.get_labels(labels)
        
        return labels

    def print_tree(self):
        print(self)

    def build_genome(self, genome):
        """
        Goes through a tree and builds a genome from all codons in the subtree.
        
        :param genome: The list of all codons in a subtree.
        :return: The fully built genome of a subtree.
        """

        if self.codon:
            # If the current node has a codon, append it to the genome.
            genome.append(self.codon)
        
        for child in self.children:
            # Recurse on all children.
            genome = child.build_genome(genome)
        
        return genome

    def build_genome_output(self, genome, output):
        """
        Recurses through a tree and builds lists of all codons and terminal
        nodes in the tree. These become the genome and phenotype of the
        individual.
        
        :param genome: The list of all codons in a subtree.
        :param output: The list of all terminal nodes in a subtree.
        :return: The lists of all codons and terminal nodes in a subtree.
        """
        
        if self.codon:
            # If the current node has a codon, append it to the genome.
            genome.append(self.codon)

        for child in self.children:
            # Recurse on all children.

            if not child.children:
                # If the current child has no children it is a terminal.
                # Append it to the output.
                output.append(child.root)
            else:
                
                genome, output = child.build_genome_output(genome, output)

        return genome, output

    def fast_genome_derivation(self, genome, index=0):
        """ Builds a tree using production choices from a given genome. Not
            guaranteed to terminate.
        """

        if index != "Incomplete" and index < len(genome):

            productions = params['BNF_GRAMMAR'].rules[self.root]
            selection = genome[index % len(genome)] % len(productions)
            chosen_prod = productions[selection]
            self.codon = genome[index % len(genome)]
            index += 1
            self.children = []

            for i in range(len(chosen_prod)):
                symbol = chosen_prod[i]
                if symbol[1] == params['BNF_GRAMMAR'].T:
                    self.children.append(Tree(symbol[0], self))

                elif symbol[1] == params['BNF_GRAMMAR'].NT:
                    self.children.append(Tree(symbol[0], self))
                    index = self.children[-1].fast_genome_derivation(genome,
                                                                     index)
        else:
            # Mapping incomplete
            return "Incomplete"
        return index

    def legal_productions(self, method, remaining_depth, productions):
        """ Returns the available production choices for a node given a depth
            limit """

        available = []

        if method == "random":
            if remaining_depth > params['BNF_GRAMMAR'].max_arity:
                available = productions
            elif remaining_depth <= 0:
                min_path = min([max([item[2] for item in prod]) for
                                prod in productions])
                shortest = [prod for prod in productions if
                            max([item[2] for item in prod]) == min_path]
                available = shortest
            else:
                for prod in productions:
                    prod_depth = max([item[2] for item in prod])
                    if prod_depth < remaining_depth:
                        available.append(prod)
                if not available:
                    min_path = min([max([item[2] for item in prod]) for
                                    prod in productions])
                    shortest = [prod for prod in productions if
                                max([item[2] for item in prod]) == min_path]
                    available = shortest

        elif method == "full":
            if remaining_depth > params['BNF_GRAMMAR'].max_arity:
                for production in productions:
                    if any(sym[3] for sym in production):
                        available.append(production)
                if not available:
                    for production in productions:
                        if not all(sym[3] for sym in production):
                            available.append(production)
            else:
                for prod in productions:
                    prod_depth = max([item[2] for item in prod])
                    if prod_depth == remaining_depth - 1:
                        available.append(prod)
                if not available:
                    # Then we don't have what we're looking for
                    for prod in productions:
                        prod_depth = 0
                        for item in prod:
                            if (item[1] == params['BNF_GRAMMAR'].NT) and \
                                    (item[2] > prod_depth):
                                prod_depth = item[2]
                        if prod_depth < remaining_depth:
                            available.append(prod)
        return available

    def check_expansion(self):
        """ Check if a given tree is completely expanded or not. Return boolean
            True if the tree IS NOT completely expanded.
        """

        # TODO: pass in list of non-terminal keys instead of doing dict
        # lookup every time.

        check = False
        if self.root in params['BNF_GRAMMAR'].non_terminals.keys():
            # Current node is a NT and should have children
            if self.children:
                # Everything is as expected
                for child in self.children:
                    check = child.check_expansion()
                    if check:
                        break
            else:
                # Current node is not completely expanded
                check = True
        return check


def generate_tree(ind_tree, genome, method, nodes, depth, max_depth,
                  depth_limit):
    """ Derive a tree using a given method """

    nodes += 1
    depth += 1
    ind_tree.id, ind_tree.depth = nodes, depth

    productions = params['BNF_GRAMMAR'].rules[ind_tree.root]
    available = ind_tree.legal_productions(method, depth_limit, productions)
    chosen_prod = choice(available)

    prod_choice = productions.index(chosen_prod)
    codon = randrange(len(productions), params['BNF_GRAMMAR'].codon_size,
                      len(productions)) + prod_choice
    ind_tree.codon = codon
    genome.append(codon)
    ind_tree.children = []

    for symbol in chosen_prod:
        if symbol[1] == params['BNF_GRAMMAR'].T:
            # if the right hand side is a terminal
            ind_tree.children.append(Tree(symbol[0], ind_tree))
        elif symbol[1] == params['BNF_GRAMMAR'].NT:
            # if the right hand side is a non-terminal
            ind_tree.children.append(Tree(symbol[0], ind_tree))
            genome, nodes, d, max_depth = \
                generate_tree(ind_tree.children[-1], genome, method, nodes,
                              depth, max_depth, depth_limit - 1)

    NT_kids = [kid for kid in ind_tree.children if kid.root in
               params['BNF_GRAMMAR'].non_terminals]

    if not NT_kids:
        # Then the branch terminates here
        depth += 1
        nodes += 1

    if depth > max_depth:
        max_depth = depth

    return genome, nodes, depth, max_depth
