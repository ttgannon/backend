/** Node: node for a singly linked list. */

class Node {
  constructor(val) {
    this.val = val;
    this.next = null;
  }
}

/** LinkedList: chained together nodes. */

class LinkedList {
  constructor(vals = []) {
    this.head = null;
    this.tail = null;
    this.length = 0;

    for (let val of vals) this.push(val);
  }

  /** push(val): add new value to end of list. */

  push(val) {
    let newNode = new Node(val);
    if (this.head === null) {
      this.head = newNode;
      this.tail = newNode;
    } else {
      this.tail.next = newNode;
      this.tail = newNode;
    }
    this.length += 1;
    
    

  }

  /** unshift(val): add new value to start of list. */

  unshift(val) {
    let newNode = new Node(val);
    if (this.head === null) {
      this.head = newNode;
      this.tail = newNode;
    } else {
      newNode.next = this.head;
      this.head = newNode;
    }
    this.length += 1;
  }

  /** pop(): return & remove last item. */

  pop() {
    if (this.head === null) {
      throw new Error('Empty list');
    }
  
    let currentNode = this.head;

    let prevNode = null;
    while (currentNode.next !== null) {
      prevNode = currentNode;
      currentNode = currentNode.next;

    }

    if (prevNode) {
      prevNode.next = null;
      this.tail = prevNode;
    } else {
      this.head = null;
      this.tail = null;
    }
  
    this.length--;
    return currentNode.val;
  }
  


  /** shift(): return & remove first item. */

  shift() {
    if (this.head === null) {
      throw new Error('Empty list');
    }
    let currentNode = this.head;
    if (currentNode.next === null) {
      this.head = null;
      this.tail = null;
      this.length--;
      return currentNode.val;
    } 
    this.head = currentNode.next;
    this.head.tail = currentNode.tail;
    this.length--;
    return currentNode.val;

  }


  /** getAt(idx): get val at idx. */

  getAt(idx) {
    if (0 > idx > this.length - 1) {
      throw new Error("Invalid index.");
    }
    if (idx === 0) {
      return this.head.val;
    }
    let currentNode = this.head;
    while (idx>0) {
      while (currentNode.next) {
        currentNode = currentNode.next;
        idx -= 1;
      }
    }
    return currentNode.val;
  }

  /** setAt(idx, val): set val at idx to val */

  setAt(idx, val) {
    if (0 > idx > this.length - 1) {
      throw new Error("Invalid index.");
    }
    if (idx === 0) {
      this.head.val = val;
      return this.head.val;
    }
    let currentNode = this.head;
    while (idx>0) {
      while (currentNode.next) {
        currentNode = currentNode.next;
        idx -= 1;
      }
    }
    currentNode.val = val;

  }

  /** insertAt(idx, val): add node w/val before idx. */

  insertAt(idx, val) {
    if (idx < 0 || idx > this.length) {
      throw new Error("Invalid index.");
    }

    let index = idx;
    let prevNode = null;
    let currentNode = this.head;
    while (index>0) {
      prevNode = currentNode;
      currentNode = currentNode.next;
      index -= 1;
    }
    const newNode = new Node(val);
    
    if (prevNode) {
      prevNode.next = newNode;
    } else {
      this.head = newNode;
    }
    newNode.next = currentNode;
    if (idx === this.length)  {
      this.tail = newNode;
    }
    this.length += 1;
    
  }

  /** removeAt(idx): return & remove item at idx, */

  removeAt(idx) {
    if (idx < 0 || idx > this.length) {
      throw new Error("Invalid index.");
    }
    let prevNode = null; 

    if (idx === 0) {
      let item = this.shift(idx);
      return item;
    }

    let currentNode = this.head;
    while (idx>0) {
      while (currentNode.next) {
        prevNode = currentNode;
        currentNode = currentNode.next;
        idx -= 1;
      }
    }
    prevNode.next = currentNode.next;
    currentNode.next = null;
    return currentNode.val;
  }

  /** average(): return an average of all values in the list */

  average() {
    if (this.length <= 0) {
      return 0;
    }
    if (this.length === 1) {
      return this.head.val;
    }
    let currentNode = this.head;
    let counter = 0;
    let sum = 0;
    while (currentNode) {
      sum += parseInt(currentNode.val);
      counter += 1;
      if (currentNode.next === null) {
        return parseFloat(sum/counter)
      }
      currentNode = currentNode.next;
    }
    
    return parseFloat(sum/counter);
  }
}

module.exports = LinkedList;
